    # -*- coding: utf-8 -*-

'''
简单的行为模型，目标：
  * 只针对单只股票
  * 支持撮合和非撮合
  * 支持深圳、上海
  * 支持有涨跌停价、无涨跌停价
  * 支持创业板价格笼子
  * 支持股票和etf

  * 尽量倾向便于FPGA硬件实现，梳理流程，不考虑面向C/C++实现
  * 将遍历全市场以验证正确性，为提升验证效率，可能用C重写一遍
  * 主要解决几个课题：
    * 撮合是否必须保存每个价格档位的链表？
    * 出快照的时机，是否必须等10ms超时？
    * 位宽检查
    * 访问次数
    * save/load
'''
from enum import Enum
import logging
import pstats
from tool.msg_util import axsbe_base, axsbe_exe, axsbe_order, axsbe_snap_stock, price_level
import tool.msg_util as msg_util
from tool.axsbe_base import SecurityIDSource_SSE, SecurityIDSource_SZSE, INSTRUMENT_TYPE
from copy import deepcopy

axob_logger = logging.getLogger(__name__)   #level 固定为 warning

#### 内部计算精度 ####
#TODO: 时戳精度和位宽 [High Priority]
APPSEQ_BIT_SIZE = 34    # 序列号，34b，约170亿
PRICE_BIT_SIZE  = 20    # 价格，20b，1048575，股票:10485.75;基金:1048.575。（若统一到3位小数则考虑用24b，则只需深圳//10）
QTY_BIT_SIZE    = 30    # 数量，30b，(1,073,741,823)，深圳2位小数，上海3位小数

PRICE_INTER_STOCK_PRECISION = 100  # 股票价格精度：2位小数，(深圳原始数据4位，上海3位)
PRICE_INTER_FUND_PRECISION  = 1000 # 基金价格精度：3位小数，(深圳原始数据4位，上海3位)

QTY_INTER_SZSE_PRECISION   = 100   # 数量精度：深圳2位小数
QTY_INTER_SSE_PRECISION    = 1000  # 数量精度：上海3位小数


class SIDE(Enum): # 2bit
    BID = 0
    ASK = 1

    UNKNOWN = -1    # 仅用于测试

class TYPE(Enum): # 2bit
    LIMIT  = 0   #限价
    MARKET = 1   #市价
    SIDE   = 2   #本方最优

    UNKNOWN = -1    # 仅用于测试

# 用于将原始精度转换到ob精度
SZSE_STOCK_PRICE_RD = msg_util.PRICE_SZSE_INCR_PRECISION // PRICE_INTER_STOCK_PRECISION
SZSE_FUND_PRICE_RD = msg_util.PRICE_SZSE_INCR_PRECISION // PRICE_INTER_FUND_PRECISION
SSE_STOCK_PRICE_RD = msg_util.PRICE_SSE_PRECISION // PRICE_INTER_STOCK_PRECISION
# SSE_FUND_PRICE_RES = msg_util.PRICE_SSE_PRECISION // PRICE_INTER_FUND_PRECISION TODO:确认精度 [low priority]

class ob_order():
    '''专注于内部使用的字段格式与位宽'''
    __slots__ = [
        'applSeqNum',
        'tradingPhase',
        'price',
        'qty',
        'side',
        'type',

        # for test olny
        'traded',
    ]

    def __init__(self, order:axsbe_order, instrument_type:INSTRUMENT_TYPE):
        # self.securityID = order.SecurityID
        self.applSeqNum = order.ApplSeqNum
        self.tradingPhase = order.TradingPhaseMarket #无需存储，目前只需要关注是否是集合竞价

        if order.SecurityIDSource==SecurityIDSource_SZSE:
            if instrument_type==INSTRUMENT_TYPE.STOCK:
                self.price = order.Price // SZSE_STOCK_PRICE_RD # 深圳 N13(4)，实际股票精度为分
            elif instrument_type==INSTRUMENT_TYPE.FUND:
                self.price = order.Price // SZSE_FUND_PRICE_RD # 深圳 N13(4)，实际基金精度为厘
            else:
                axob_logger.error(f'order SZSE ApplSeqNum={order.ApplSeqNum} instrument_type={instrument_type} not support!')
        elif order.SecurityIDSource==SecurityIDSource_SSE:
            if instrument_type==INSTRUMENT_TYPE.STOCK:
                self.price = order.Price // SSE_STOCK_PRICE_RD # 上海 原始数据3位小数
            else:
                axob_logger.error(f'order SSE ApplSeqNum={order.ApplSeqNum} instrument_type={instrument_type} not support!')
        else:
            self.price = 0
        self.traded = False #仅用于测试：市价单，当有成交后，市价单的价格将确定

        self.qty = order.OrderQty    # 上海 3位小数

        if order.Side_str=='买入':
            self.side = SIDE.BID
        elif order.Side_str=='卖出':
            self.side = SIDE.ASK
        else:   #TODO: 映射上海 [low priority]
            self.side = SIDE.UNKNOWN

        if order.Type_str=='限价':
            self.type = TYPE.LIMIT
        elif order.Type_str=='市价':
            self.type = TYPE.MARKET
        elif order.Type_str=='本方最优':
            self.type = TYPE.SIDE
        else:   #TODO: 映射上海 [low priority]
            self.type = TYPE.UNKNOWN

        ## 位宽及精度舍入可行性检查
        if self.applSeqNum >= (1<<APPSEQ_BIT_SIZE) and self.applSeqNum!=0xffffffffffffffff:
            axob_logger.error(f'{order.SecurityID:06d} order ApplSeqNum={order.ApplSeqNum} ovf!')

        if self.price >= (1<<PRICE_BIT_SIZE):
            axob_logger.error(f'{order.SecurityID:06d} order ApplSeqNum={order.ApplSeqNum} Price={order.Price} ovf!')  # 无涨跌停价时可能，即使限价单也可能溢出，且会被前端处理成0x7fff_ffff

        if self.qty >= (1<<QTY_BIT_SIZE):
            axob_logger.error(f'{order.SecurityID:06d} order ApplSeqNum={order.ApplSeqNum} Volumn={order.OrderQty} ovf!')

        if self.type==TYPE.LIMIT:   #检查限价单价格是否溢出；市价单价格是无效值，不可参与检查
            if order.SecurityIDSource==SecurityIDSource_SZSE:
                if instrument_type==INSTRUMENT_TYPE.STOCK and order.Price % SZSE_STOCK_PRICE_RD:
                    axob_logger.error(f'{order.SecurityID:06d} order SZSE STOCK ApplSeqNum={order.ApplSeqNum} Price={order.Price} precision dnf!')  #当被前端处理成0x7fff_ffff时 会有余数
                elif instrument_type==INSTRUMENT_TYPE.FUND and order.Price % SZSE_FUND_PRICE_RD:
                    axob_logger.error(f'{order.SecurityID:06d} order SZSE FUND ApplSeqNum={order.ApplSeqNum} Price={order.Price} precision dnf!')  #当被前端处理成0x7fff_ffff时 会有余数
            elif order.SecurityIDSource==SecurityIDSource_SSE:
                if instrument_type==INSTRUMENT_TYPE.STOCK and order.Price % SSE_STOCK_PRICE_RD:
                    axob_logger.error(f'{order.SecurityID:06d} order SSE STOCK ApplSeqNum={order.ApplSeqNum} Price={order.Price} precision dnf!')

    def __str__(self) -> str:
        return f'{self.applSeqNum}'

    def save(self):
        '''save/load 用于保存/加载测试时刻'''
        data = {}
        for attr in self.__slots__:
            value = getattr(self, attr)
            data[attr] = value
        return data

    def load(self, data):
        for attr in self.__slots__:
            setattr(self, attr, data[attr])



class ob_cancel():
    '''专注于内部使用的字段格式与位宽'''
    def __init__(self, ApplSeqNum, Qty, Price, Side, TradingPhaseMarket, SecurityIDSource, instrument_type, SecurityID):
        self.applSeqNum = ApplSeqNum
        self.qty = Qty
        if SecurityIDSource==SecurityIDSource_SZSE:
            if instrument_type==INSTRUMENT_TYPE.STOCK:
                self.price = Price // SZSE_STOCK_PRICE_RD # 深圳 N13(4)，实际股票精度为分
            elif instrument_type==INSTRUMENT_TYPE.FUND:
                self.price = Price // SZSE_FUND_PRICE_RD # 深圳 N13(4)，实际基金精度为厘
            else:
                axob_logger.error(f'{SecurityID:06d} cancel SZSE ApplSeqNum={ApplSeqNum} instrument_type={instrument_type} not support!')
        elif SecurityIDSource==SecurityIDSource_SSE:
            if instrument_type==INSTRUMENT_TYPE.STOCK:
                self.price = Price // SSE_STOCK_PRICE_RD # 上海 原始数据3位小数
            else:
                axob_logger.error(f'{SecurityID:06d} cancel SSE ApplSeqNum={ApplSeqNum} instrument_type={instrument_type} not support!')
        else:
            axob_logger.error(f'{SecurityID:06d} cancel ApplSeqNum={ApplSeqNum} SecurityIDSource={SecurityIDSource} unknown!')
        self.side = Side
        self.tradingPhase = TradingPhaseMarket #无需存储，目前只需要关注是否是集合竞价

        if self.applSeqNum >= (1<<APPSEQ_BIT_SIZE):
            axob_logger.error(f'{SecurityID:06d} cancel ApplSeqNum={ApplSeqNum} ovf!')

        if self.price >= (1<<PRICE_BIT_SIZE):
            axob_logger.error(f'{SecurityID:06d} cancel ApplSeqNum={ApplSeqNum} Price={Price} ovf!')

        if self.qty >= (1<<QTY_BIT_SIZE):
            axob_logger.error(f'{SecurityID:06d} cancel ApplSeqNum={ApplSeqNum} Volumn={Qty} ovf!')

    def __str__(self) -> str:
        return f'{self.applSeqNum}'


class level_node():
    __slots__ = [
        'price',
        'qty',

        # for test olny
        'ts',
    ]
    def __init__(self, price, qty, ts):
        self.price = price
        self.qty = qty

        # 目前没用，仅供调试
        self.ts = [ts]

    def save(self):
        '''save/load 用于保存/加载测试时刻'''
        data = {}
        for attr in self.__slots__:
            value = getattr(self, attr)
            if attr=='ts':
                data[attr] = deepcopy(value)
            else:
                data[attr] = value
        return data

    def load(self, data):
        for attr in self.__slots__:
            setattr(self, attr, data[attr])


class AXOB():
    __slots__ = [
        'SecurityID',
        'SecurityIDSource',
        'instrument_type',

        'order_map',    # map of ob_order
        'bid_level_tree', # map of level_node
        'ask_level_tree', # map of level_node

        'NumTrades',
        'bid_max_level_price',
        'bid_max_level_qty',
        'ask_min_level_price',
        'ask_min_level_qty',
        'LastPx',
        'HighPx',
        'LowPx',
        'OpenPx',

        'ChannelNo',
        'PrevClosePx',
        'DnLimitPx',
        'UpLimitPx',
        'current_inc_timestamp',
        'BidWeightSize',
        'BidWeightValue',
        'AskWeightSize',
        'AskWeightValue',

        'TotalVolumeTrade',
        'TotalValueTrade',

        'holding_order',
        'holding_nb',

        'TradingPhaseMarket',

        # for test olny
        'msg_nb',
        'rebuilt_snaps',    # list of snap
        'market_snaps',     # list of snap
        'last_snap',
        'last_inc_applSeqNum',

        'logger',
        'DBG',
        'INFO',
        'WARN',
        'ERR',
    ]
    def __init__(self, SecurityID:int, SecurityIDSource, instrument_type:INSTRUMENT_TYPE):
        '''
        '''
        self.SecurityID = SecurityID
        self.SecurityIDSource = SecurityIDSource #"证券代码源101=上交所;102=深交所;103=香港交易所" 在hls中用宏或作为模板参数设置
        self.instrument_type = instrument_type

        ## 结构数据：
        self.order_map = {} #订单队列，以applSeqNum作为索引
        self.bid_level_tree = {} #买方价格档，以价格作为索引
        self.ask_level_tree = {} #卖方价格档

        self.NumTrades = 0
        self.bid_max_level_price = 0
        self.bid_max_level_qty = 0
        self.ask_min_level_price = 0
        self.ask_min_level_qty = 0
        self.LastPx = 0
        self.HighPx = 0
        self.LowPx = 0
        self.OpenPx = 0

        self.ChannelNo = 0 #来自于快照
        self.PrevClosePx = 0 #来自于快照 深圳要处理到内部精度，用于在还原快照时比较
        self.DnLimitPx = 0  # #来自于快照 TODO: cover: 无涨跌停价 [low priority]
        self.UpLimitPx = 0  # #来自于快照 TODO: cover: 无涨跌停价 [low priority]
        self.current_inc_timestamp = 0 #来自于逐笔
        
        self.BidWeightSize = 0
        self.BidWeightValue = 0
        self.AskWeightSize = 0
        self.AskWeightValue = 0

        self.TotalVolumeTrade = 0
        self.TotalValueTrade = 0

        self.holding_order = None
        self.holding_nb = 0

        self.TradingPhaseMarket = axsbe_base.TPM.Starting

        ## 调试数据，仅用于测试算法是否正确：
        self.msg_nb = 0
        self.rebuilt_snaps = []
        self.market_snaps = []
        self.last_snap = None
        self.last_inc_applSeqNum = 0

        ## 日志
        self.logger = logging.getLogger(f'{self.SecurityID:06d}')
        g_logger = logging.getLogger('main')
        self.logger.setLevel(g_logger.getEffectiveLevel())
        for h in g_logger.handlers:
            self.logger.addHandler(h)
            axob_logger.addHandler(h) #这里补上模块日志的handler，有点ugly TODO: better way [low prioryty]

        self.DBG = self.logger.debug
        self.INFO = self.logger.info
        self.WARN = self.logger.warning
        self.ERR = self.logger.error

    def onMsg(self, msg):
        '''处理总入口'''
        if isinstance(msg, axsbe_order) or isinstance(msg, axsbe_exe) or isinstance(msg, axsbe_snap_stock):
            if msg.SecurityID!=self.SecurityID:
                return

            self.TradingPhaseMarket = msg.TradingPhaseMarket #TODO:是否区分快照和逐笔？等测试情况，需要看二者的时间关系 [High priority]

            if isinstance(msg, axsbe_order) or isinstance(msg, axsbe_exe):
                self.current_inc_timestamp = msg.TransactTime    #只用逐笔

            if isinstance(msg, axsbe_order):
                self.onOrder(msg)
            elif isinstance(msg, axsbe_exe):
                self.onExec(msg)
            else:# isinstance(msg, axsbe_snap_stock):
                self.onSnap(msg)

            if isinstance(msg, axsbe_order) or isinstance(msg, axsbe_exe):
                self.last_inc_applSeqNum = msg.ApplSeqNum
        else:
            pass

        ## 调试数据，仅用于测试算法是否正确：
        self.msg_nb += 1

        if len(self.ask_level_tree):
            assert self.ask_min_level_price==min(self.ask_level_tree.keys()), f'{self.SecurityID} cache ask-min-price NG'
            assert self.ask_min_level_qty==min(self.ask_level_tree.items(), key=lambda x: x[0])[1].qty, f'{self.SecurityID} cache ask-min-qty NG'
        if len(self.bid_level_tree):
            assert self.bid_max_level_price==max(self.bid_level_tree.keys()), f'{self.SecurityID} cache bid-max-price NG'
            assert self.bid_max_level_qty==max(self.bid_level_tree.items(), key=lambda x: x[0])[1].qty, f'{self.SecurityID} ache bid-max-qty NG'

    def onOrder(self, order:axsbe_order):
        '''
        逐笔订单入口，统一提取市价单、限价单的关键字段到内部订单格式
        跳转到处理限价单或处理撤单
        TODO: SSE的撤单也在order，跳转到onCancel [low priority]
        '''
        self.DBG(f'msg#{self.msg_nb} onOrder:{order}')
        if self.SecurityIDSource == SecurityIDSource_SZSE:
            _order = ob_order(order, self.instrument_type)
        elif self.SecurityIDSource == SecurityIDSource_SSE:
            pass # TODO: order or cancel [Low Priority]
        else:
            return

        if _order.type==TYPE.MARKET:
            # 市价单，都必须在开盘之后
            if self.bid_max_level_qty==0 and self.ask_min_level_qty==0:
                self.ERR('未定义模式:市价单早于价格档') #TODO: cover [Mid priority]
            #if _order.type==TYPE.MARKET:
                # 市价单，几种可能：
                #    * 对手方最优价格申报：有成交、最后挂在对方一档或者二档
                #    * 最优五档即时成交剩余撤销申报：最后有撤单
                #    * 即时成交剩余撤销申报：最后有撤单
                #    * 全额成交或撤销申报：最后有撤单
            if _order.type==TYPE.SIDE:
                # 本方最优价格申报 转限价单
                if _order.side==SIDE.BID:
                    if self.bid_max_level_price!=0 and self.bid_max_level_qty!=0:   #本方有量
                        _order.price = self.bid_max_level_price
                    else:
                        _order.price = self.DnLimitPx
                        axob_logger.error(f'order #{_order.applSeqNum} 本方最优买单 但无本方价格!') #TODO: cover [Mid priority]
                else:
                    if self.ask_min_level_price!=0 and self.ask_min_level_qty!=0:   #本方有量
                        _order.price = self.ask_min_level_price
                    else:
                        _order.price = self.UpLimitPx
                        axob_logger.error(f'order #{_order.applSeqNum} 本方最优卖单 但无本方价格!') #TODO: cover [Mid priority]
        self.onLimitOrder(_order)


    def onLimitOrder(self, order:ob_order):
        if order.tradingPhase == axsbe_base.TPM.OpenCall or order.tradingPhase == axsbe_base.TPM.CloseCall: #集合竞价期间，直接插入；暂时还是用order的TPM，而非自身的； TODO:决定用哪个 [High priority]
            self.insertOrder(order)
            self.genSnap()   #可出snap
        else:
            #把此前缓存的订单(市价/限价)插入LOB
            if self.holding_nb != 0:
                if self.holding_order.type == TYPE.MARKET and not self.holding_order.traded:
                    self.ERR(f'市价单 {self.holding_order} 未伴随成交')

                self.insertOrder(self.holding_order)
                self.holding_nb = 0

                self.genSnap()   #先出一个snap

            #若是可能成交的限价单，则缓存住，等成交
            if (order.side == SIDE.BID and (order.price >= self.bid_max_level_price and self.bid_max_level_qty > 0)) or \
               (order.side == SIDE.ASK and (order.price <= self.ask_min_level_price and self.ask_min_level_qty > 0)):
                self.holding_order = order
                self.holding_nb += 1
            else:
                self.insertOrder(order)

                self.genSnap()   #再出一个snap

    def insertOrder(self, order:ob_order):
        '''
        订单入列，更新对应的价格档位数据
        '''
        self.order_map[order.applSeqNum] = order
        
        if order.side == SIDE.BID:
            # self.bidPriceCacheHandler.addQty(order.price, order.qty)
            if order.price in self.bid_level_tree:
                self.bid_level_tree[order.price].qty += order.qty
                self.bid_level_tree[order.price].ts.append(order.applSeqNum)
                if order.price==self.bid_max_level_price:
                    self.bid_max_level_qty += order.qty
            else:
                node = level_node(order.price, order.qty, order.applSeqNum)
                self.bid_level_tree[order.price] = node

                if self.bid_max_level_qty==0 or node.price > self.bid_max_level_price:  #买方出现更高价格
                    self.bid_max_level_price = order.price
                    self.bid_max_level_qty = order.qty

            self.BidWeightSize += order.qty
            self.BidWeightValue += order.price * order.qty
        elif order.side == SIDE.ASK:
            # self.askPriceCacheHandler.addQty(order.price, order.qty)
            if order.price in self.ask_level_tree:
                self.ask_level_tree[order.price].qty += order.qty
                self.ask_level_tree[order.price].ts.append(order.applSeqNum)
                if order.price==self.ask_min_level_price:
                    self.ask_min_level_qty += order.qty
            else:
                node = level_node(order.price, order.qty, order.applSeqNum)
                self.ask_level_tree[order.price] = node

                if self.ask_min_level_qty==0 or node.price < self.ask_min_level_price: #卖方出现更低价格
                    self.ask_min_level_price = order.price
                    self.ask_min_level_qty = order.qty

            self.AskWeightSize += order.qty
            self.AskWeightValue += order.price * order.qty

    def onExec(self, exec:axsbe_exe):
        '''
        逐笔成交入口
        跳转到处理成交或处理撤单
        '''
        self.DBG(f'msg#{self.msg_nb} onExec:{exec}')
        if exec.ExecType_str=='成交' or self.SecurityIDSource==SecurityIDSource_SSE:
            self.onTrade(exec)
        else:
            #only SecurityIDSource_SZSE
            if exec.BidApplSeqNum!=0:  # 撤销bid
                cancel_seq = exec.BidApplSeqNum
                Side = SIDE.BID
            else:   # 撤销ask
                cancel_seq = exec.OfferApplSeqNum
                Side = SIDE.ASK
            _cancel = ob_cancel(cancel_seq, exec.LastQty, exec.LastPx, Side, exec.TradingPhaseMarket, self.SecurityIDSource, self.instrument_type, self.SecurityID)
            self.onCancel(_cancel)



    def onTrade(self, exec:axsbe_exe):
        pass
    
    def onCancel(self, cancel:ob_cancel):
        '''
        处理撤单，来自深交所逐笔成交或上交所逐笔成交
        撤销此前缓存的订单(市价/限价)，或插入LOB
        '''
        if self.holding_nb != 0:    #TODO: 此时不应有holding [high priority]
            self.holding_nb = 0
            if self.holding_order.applSeqNum != cancel.applSeqNum: #撤销的不是缓存单，把缓存单插入LOB
                self.insertOrder(self.holding_order)
                
                self.genSnap()   #先出一个snap
            else:
                return  #撤销缓存单，holding_nb清空即可

        order = self.order_map.pop(cancel.applSeqNum)   # 注意order.qty是旧值

        if cancel.side == SIDE.BID:
            self.bid_level_tree[order.price].qty -= cancel.qty
            self.bid_level_tree[order.price].ts.remove(order.applSeqNum)
            if order.price==self.bid_max_level_price:
                self.bid_max_level_qty -= cancel.qty

            if self.bid_level_tree[order.price].qty==0:
                self.bid_level_tree.pop(order.price)

                if order.price==self.bid_max_level_price:  #买方最高价被cancel光
                    self.bid_max_level_qty = 0
                    # locate next lower bid level
                    for p, l in sorted(self.bid_level_tree.items(),key=lambda x:x[0], reverse=True):    #从大到小遍历
                        if p<self.bid_max_level_price:
                            self.bid_max_level_price = p
                            self.bid_max_level_qty = l.qty
                            break

            self.BidWeightSize -= cancel.qty
            self.BidWeightValue -= order.price * cancel.qty
        elif order.side == SIDE.ASK:
            self.ask_level_tree[order.price].qty -= cancel.qty
            self.ask_level_tree[order.price].ts.remove(order.applSeqNum)
            if order.price==self.ask_min_level_price:
                self.ask_min_level_qty -= cancel.qty

            if self.ask_level_tree[order.price].qty==0:
                self.ask_level_tree.pop(order.price)

                if order.price==self.ask_min_level_price:  #卖方最低价被cancel光
                    # locate next higher ask level
                    self.ask_min_level_qty = 0
                    for p, l in sorted(self.ask_level_tree.items(),key=lambda x:x[0], reverse=False):    #从小到大遍历
                        if p>self.ask_min_level_price:
                            self.ask_min_level_price = p
                            self.ask_min_level_qty = l.qty
                            break

            self.AskWeightSize -= cancel.qty
            self.AskWeightValue -= order.price * cancel.qty

        self.genSnap()   #缓存单成交完
        

    def onSnap(self, snap:axsbe_snap_stock):
        self.DBG(f'msg#{self.msg_nb} onSnap:{snap}')
        if snap.TradingPhaseSecurity != axsbe_base.TPI.Normal:
            self.ERR(f'TradingPhaseSecurity={axsbe_base.TPI.str(snap.TradingPhaseSecurity)}')
            return

        ## 更新常量
        if self.ChannelNo==0:
            self.INFO(f"Update constatant: ChannelNo={snap.ChannelNo}, PrevClosePx={snap.PrevClosePx}, UpLimitPx={snap.UpLimitPx}, DnLimitPx={snap.DnLimitPx}")
        self.ChannelNo = snap.ChannelNo
        if self.SecurityIDSource==SecurityIDSource_SZSE:
            if self.instrument_type==INSTRUMENT_TYPE.STOCK:
                self.PrevClosePx = snap.PrevClosePx // (msg_util.PRICE_SZSE_SNAP_PRECLOSE_PRECISION//PRICE_INTER_STOCK_PRECISION)
            elif self.instrument_type==INSTRUMENT_TYPE.FUND:
                self.PrevClosePx = snap.PrevClosePx // (msg_util.PRICE_SZSE_SNAP_PRECLOSE_PRECISION//PRICE_INTER_FUND_PRECISION)
            else:
                pass    # TODO:
        else:
            pass #TODO:

        self.UpLimitPx = snap.UpLimitPx
        self.DnLimitPx = snap.DnLimitPx

        ## 检查重建算法，仅用于测试算法是否正确：
        snap._seq = self.msg_nb
        if snap.TradingPhaseMarket<axsbe_base.TPM.OpenCall:
            pass
        else:
            # 在重建的快照中检索是否有相同的快照
            if self.last_snap and snap.is_same(self.last_snap) and self._chkSnapTimestamp(snap.TransactTime, self.last_snap.TransactTime):
                self.INFO(f'snap #{self.msg_nb} matches last genSnap #{self.last_snap._seq}')
                self.rebuilt_snaps = []
                #这里不丢弃last_snap，因为可能无逐笔数据而导致快照不更新
            else:
                matched = False
                for match_idx in range(len(self.rebuilt_snaps)):
                    gen = self.rebuilt_snaps[match_idx]
                    if snap.is_same(gen) and self._chkSnapTimestamp(snap.TransactTime, gen.TransactTime):
                        self.INFO(f'market snap #{self.msg_nb} matches history rebuilt snap #{gen._seq}')
                        matched = True
                        break
                
                if matched: 
                    self.rebuilt_snaps = self.rebuilt_snaps[match_idx+1:]   #丢弃已匹配的
                else:
                    self.market_snaps.append(snap) #缓存交易所快照
                    self.WARN(f'market snap #{self.msg_nb} not found in history rebuilt snaps!')

                    # self.WARN('breakpoint4')
                    # for p, l in sorted(self.ask_level_tree.items(),key=lambda x:x[0], reverse=True):    #从大到小遍历
                    #     # self.DBG(f'ask\t{p}\t{l.qty}\t{l.ts}')
                    #     self.DBG(f'ask\t{p}\t{l.qty}')
                    # for p, l in sorted(self.bid_level_tree.items(),key=lambda x:x[0], reverse=True):    #从大到小遍历
                    #     # self.DBG(f'bid\t{p}\t{l.qty}\t{l.ts}')
                    #     self.DBG(f'bid\t{p}\t{l.qty}')



    def genSnap(self):
        assert self.holding_nb==0, 'genSnap but with holding'

        snap = None
        if self.TradingPhaseMarket < axsbe_base.TPM.OpenCall or self.TradingPhaseMarket > axsbe_base.TPM.CloseCall:
            # 无需生成
            pass
        elif self.TradingPhaseMarket==axsbe_base.TPM.OpenCall or self.TradingPhaseMarket==axsbe_base.TPM.CloseCall:
            # 集合竞价快照
            snap = self.genCallSnap()
        else:
            # 连续竞价快照
            snap = self.genTradingSnap()
            

        ## 调试数据，仅用于测试算法是否正确：
        if snap is not None:
            self.DBG(snap)
            snap._seq = self.msg_nb # 用于调试
            self.last_snap = snap

            #在收到的交易所快照中查找是否有一样的
            matched = False
            for match_idx in range(len(self.market_snaps)):
                rcv = self.market_snaps[match_idx]
                if snap.is_same(rcv) and self._chkSnapTimestamp(rcv.TransactTime, snap.TransactTime):
                    self.WARN(f'rebuilt snap #{self.msg_nb} matches history market snap #{rcv._seq}') # 重建快照在市场快照之后，属于警告
                    matched = True
                    break
            
            if matched: 
                self.market_snaps.pop(match_idx)    #丢弃已匹配的
            else:
                self.rebuilt_snaps.append(snap)     #无历史的才缓存，有历史的只放进last_snap


                


    def genCallSnap(self, show_level_nb=10, show_potential=False):
        '''
        show_level_nb:  展示的价格档数
        show_potential: 在无法撮合时展示出双方价格档
        '''
        # if self.msg_nb==750:
        #     self.WARN('breakpoint2')
        #     for p, l in sorted(self.ask_level_tree.items(),key=lambda x:x[0], reverse=True):    #从大到小遍历
        #         self.DBG(f'ask\t{p}\t{l.qty}\t{l.ts}')
        #     for p, l in sorted(self.bid_level_tree.items(),key=lambda x:x[0], reverse=True):    #从大到小遍历
        #         self.DBG(f'bid\t{p}\t{l.qty}\t{l.ts}')


        #1. 查找 最低卖出价格档、最高买入价格档
        _bid_max_level_price = self.bid_max_level_price
        _bid_max_level_qty = self.bid_max_level_qty
        _ask_min_level_price = self.ask_min_level_price
        _ask_min_level_qty = self.ask_min_level_qty

        #2. 初始 撮合成交价
        if _bid_max_level_qty==0 and _ask_min_level_qty==0: #两边都无委托
            price = 0
        else: # 至少一边存在委托
            if _bid_max_level_qty==0:
                price = _ask_min_level_price
            elif _ask_min_level_qty==0:
                price = _bid_max_level_price
            else:   #两边都存在，双方最优价可能交叉也可能无交叉
                price = 0

        
        #3. 初始 总成交数量 = 0
        volumeTrade = 0
        bid_Qty = 0
        bid_trade_level_nb = 0
        ask_Qty = 0
        ask_trade_level_nb = 0
        
        #4. 撮合循环：
        while _bid_max_level_qty!=0 and _ask_min_level_qty!=0:  # 双方均有最优委托
            if _bid_max_level_price >= _ask_min_level_price:    # 双方最优价有交叉
                if bid_Qty == 0:
                    bid_Qty = _bid_max_level_qty
                if ask_Qty == 0:
                    ask_Qty = _ask_min_level_qty
                if bid_Qty >= ask_Qty:
                    volumeTrade += ask_Qty
                    bid_Qty -= ask_Qty
                    ask_Qty = 0

                    ask_trade_level_nb += 1
                    if bid_Qty==ask_Qty:
                        bid_trade_level_nb += 1
                else:
                    volumeTrade += bid_Qty
                    ask_Qty -= bid_Qty
                    bid_Qty = 0

                    bid_trade_level_nb += 1

                if bid_Qty == 0 and ask_Qty == 0:   # 恰好双方数量相等。 
                    if _bid_max_level_price>=self.PrevClosePx and _ask_min_level_price<=self.PrevClosePx:   #
                        price = self.PrevClosePx
                    else:
                        if abs(_bid_max_level_price-self.PrevClosePx) < abs(_ask_min_level_price-self.PrevClosePx):
                            price = _bid_max_level_price
                        else:
                            price = _ask_min_level_price

                if bid_Qty == 0:
                    if ask_Qty != 0:
                        price = _ask_min_level_price
                    # locate next lower bid level
                    _bid_max_level_qty = 0
                    for p, l in sorted(self.bid_level_tree.items(),key=lambda x:x[0], reverse=True):    #从大到小遍历
                        if p<_bid_max_level_price:
                            # if price<=p:
                            #     price = p+1
                            _bid_max_level_price = p
                            _bid_max_level_qty = l.qty
                            break

                if ask_Qty == 0:
                    if bid_Qty != 0:
                        price = _bid_max_level_price
                    # locate next higher ask level
                    _ask_min_level_qty = 0
                    for p, l in sorted(self.ask_level_tree.items(),key=lambda x:x[0], reverse=False):    #从小到大遍历
                        if p>_ask_min_level_price:
                            # if price>=p:
                            #     price = p-1
                            _ask_min_level_price = p
                            _ask_min_level_qty = l.qty
                            break

            else:   #后续买卖双方均有委托，但价格无交叉
                if ask_Qty==0 and bid_Qty==0:   # 双方恰好成交，根据下一档价格，可能需要修正成交价
                    if _ask_min_level_qty and price>=_ask_min_level_price: #成交价高于卖方下一档，必须修正到小于等于卖方下一档
                        if _bid_max_level_price+1<_ask_min_level_price:    # 买方下一档+1分钱 小于 卖方下一档，修到卖方下一档-1
                            price = _ask_min_level_price-1
                        else:
                            if _ask_min_level_qty <= _bid_max_level_qty:   # 卖方双方下一档只差一分钱，选量小的，同量卖方优先
                                price = _ask_min_level_price
                                ask_Qty = _ask_min_level_qty
                            else:
                                price = _bid_max_level_price
                                bid_Qty = _bid_max_level_qty

                    elif _bid_max_level_qty and price<=_bid_max_level_price: #成交价低于买方下一档，必须修正到大于等于买方下一档
                        if _ask_min_level_price>_bid_max_level_price+1: # 卖方下一档分钱 大于 买方下一档+1，修到买方下一档+1
                            price = _bid_max_level_price+1
                        else:
                            if _bid_max_level_qty <= _ask_min_level_qty: # 卖方双方下一档只差一分钱，选量小的，同量买方优先
                                price = _bid_max_level_price
                                bid_Qty = _bid_max_level_qty
                            else:
                                price = _ask_min_level_price
                                ask_Qty = _ask_min_level_qty
                   
                break


        # 填充成交信息
        self.TotalVolumeTrade = volumeTrade

        # TotalValueTrade 计算与小数位数扩展
        if self.SecurityIDSource==SecurityIDSource_SZSE:
            # 乘法输入：深圳(Qty精度2位、price精度2位or3位小数)；输出TotalValueTrade深圳(精度4位小数)
            if self.instrument_type==INSTRUMENT_TYPE.STOCK:
                self.TotalValueTrade = int(volumeTrade * price/(QTY_INTER_SZSE_PRECISION*PRICE_INTER_STOCK_PRECISION // msg_util.TOTALVALUETRADE_SZSE_PRECISION)) # 2x2->4
            elif self.instrument_type==INSTRUMENT_TYPE.FUND:
                self.TotalValueTrade = int(volumeTrade * price/(QTY_INTER_SZSE_PRECISION*PRICE_INTER_FUND_PRECISION // msg_util.TOTALVALUETRADE_SZSE_PRECISION)) # 2x3->4
            else:
                self.TotalValueTrade = None
        elif self.SecurityIDSource==SecurityIDSource_SSE:
            # 乘法输入：上海(Qty精度3位、price精度2位or3位小数)；输出TotalValueTrade上海(精度5位小数)
            if self.instrument_type==INSTRUMENT_TYPE.STOCK:
                self.TotalValueTrade = int(volumeTrade * price/(QTY_INTER_SSE_PRECISION*PRICE_INTER_STOCK_PRECISION // msg_util.TOTALVALUETRADE_SSE_PRECISION)) # 3x2 -> 5
            elif self.instrument_type==INSTRUMENT_TYPE.FUND:
                self.TotalValueTrade = int(volumeTrade * price/(QTY_INTER_SSE_PRECISION*PRICE_INTER_FUND_PRECISION // msg_util.TOTALVALUETRADE_SZSE_PRECISION)) # 3x3->5
            else:
                self.TotalValueTrade = None
        else:
            self.TotalValueTrade = None

        # price 小数位数扩展
        price = self._fmtPrice_inter2snap(price)

        # 价格档
        snap_ask_levels = {}
        snap_bid_levels = {}
        if volumeTrade == 0: # 无法撮合时
            if not show_potential:
                for i in range(0, show_level_nb):
                    snap_ask_levels[i] = price_level(0,0)
                    snap_bid_levels[i] = price_level(0,0)
            else:   #无法撮合时，揭示多档
                snap_ask_levels, snap_bid_levels = self._getLevels(show_level_nb)
        else: #可撮合时，揭示2档
            snap_ask_levels[0] = price_level(price, volumeTrade)
            snap_ask_levels[1] = price_level(0, ask_Qty)
            for i in range(2, show_level_nb):
                snap_ask_levels[i] = price_level(0,0)

            snap_bid_levels[0] = price_level(price, volumeTrade)
            snap_bid_levels[1] = price_level(0, bid_Qty)
            for i in range(2, show_level_nb):
                snap_bid_levels[i] = price_level(0,0)


        #### 开始构造快照
        if self.instrument_type==INSTRUMENT_TYPE.STOCK:
            snap_call = axsbe_snap_stock(SecurityIDSource=self.SecurityIDSource, source=f"genSnap-call")
        else:
            return None # TODO: not ready [Mid priority]
        
        # 固定参数
        snap_call.SecurityID = self.SecurityID
        if self.SecurityIDSource==SecurityIDSource_SZSE:
            if self.instrument_type==INSTRUMENT_TYPE.STOCK:
                snap_call.PrevClosePx = self.PrevClosePx * (msg_util.PRICE_SZSE_SNAP_PRECLOSE_PRECISION//PRICE_INTER_STOCK_PRECISION)
            elif self.instrument_type==INSTRUMENT_TYPE.FUND:
                snap_call.PrevClosePx = self.PrevClosePx * (msg_util.PRICE_SZSE_SNAP_PRECLOSE_PRECISION//PRICE_INTER_FUND_PRECISION)
            else:
                snap_call.PrevClosePx = self.PrevClosePx    #TODO:
        else:
            snap_call.PrevClosePx = self.PrevClosePx    #TODO:
            
        snap_call.UpLimitPx = self.UpLimitPx
        snap_call.DnLimitPx = self.DnLimitPx
        snap_call.ChannelNo = self.ChannelNo

        # 本地维护参数
        snap_call.ask = snap_ask_levels
        snap_call.bid = snap_bid_levels
        snap_call.NumTrades = 0#self.NumTrades
        snap_call.TotalVolumeTrade = 0#self.TotalVolumeTrade
        snap_call.TotalValueTrade = 0#self.TotalValueTrade
        snap_call.LastPx = 0#self.LastPx
        snap_call.HighPx = 0#self.HighPx
        snap_call.LowPx = 0#self.LowPx
        snap_call.OpenPx = 0#self.OpenPx
        

        # 本地维护参数
        snap_call.BidWeightPx = 0   #开盘撮合时期为0
        snap_call.BidWeightSize = 0
        snap_call.AskWeightPx = 0
        snap_call.AskWeightSize = 0

        snap_call.TransactTime = self.current_inc_timestamp #最新的一个逐笔消息时戳

        snap_call.update_TradingPhaseCode(self.TradingPhaseMarket, axsbe_base.TPI.Normal)

        return snap_call
        

    def genTradingSnap(self):
        return

    def _fmtPrice_inter2snap(self, price):
        # price 小数位数扩展
        if self.SecurityIDSource==SecurityIDSource_SZSE:
            # 深圳快照价格精度6位小数（唯有PrevClosePx是4位小数）
            if self.instrument_type==INSTRUMENT_TYPE.STOCK:
                price *= msg_util.PRICE_SZSE_SNAP_PRECISION // PRICE_INTER_STOCK_PRECISION    # 内部2位，输出6位
            elif self.instrument_type==INSTRUMENT_TYPE.FUND:
                price *= msg_util.PRICE_SZSE_SNAP_PRECISION // PRICE_INTER_FUND_PRECISION    # 内部3位，输出6位
            else:
                price = None
        elif self.SecurityIDSource==SecurityIDSource_SSE:
            # 上海快照价格精度3位小数
            if self.instrument_type==INSTRUMENT_TYPE.STOCK:
                price *= msg_util.PRICE_SSE_PRECISION // PRICE_INTER_STOCK_PRECISION    # 内部2位，输出3位
            elif self.instrument_type==INSTRUMENT_TYPE.FUND:
                price *= msg_util.PRICE_SSE_PRECISION // PRICE_INTER_FUND_PRECISION    # 内部3位，输出3位
            else:
                price = None
        else:
            price = None
        return price


    def _getLevels(self, level_nb):
        '''
        输出：卖方最优n档, 买方最优n档
        '''
        snap_ask_levels = {}
        snap_bid_levels = {}
        
        _bid_max_level_price = self.bid_max_level_price
        _bid_max_level_qty = self.bid_max_level_qty
        _ask_min_level_price = self.ask_min_level_price
        _ask_min_level_qty = self.ask_min_level_qty

        for nb in range(level_nb):
            if _ask_min_level_qty!=0:
                snap_ask_levels[nb] = price_level(self._fmtPrice_inter2snap(_ask_min_level_price), _ask_min_level_qty)
                # snap_ask_levels[nb].addQ(ask_min_level.orderList, order_nb) #TODO: order_link [Mid priority]
                # locate next higher ask level
                _ask_min_level_qty = 0
                for p, l in sorted(self.ask_level_tree.items(),key=lambda x:x[0], reverse=False):    #从小到大遍历
                    if p>_ask_min_level_price:
                        _ask_min_level_price = p
                        _ask_min_level_qty = l.qty
                        break
            else:
                snap_ask_levels[nb] = price_level(0,0)

            if _bid_max_level_qty!=0:
                snap_bid_levels[nb] = price_level(self._fmtPrice_inter2snap(_bid_max_level_price), _bid_max_level_qty)
                # snap_bid_levels[nb].addQ(bid_max_level.orderList, order_nb) #TODO: order_link [Mid priority]
                # locate next lower bid level
                _bid_max_level_qty = 0
                for p, l in sorted(self.bid_level_tree.items(),key=lambda x:x[0], reverse=True):    #从大到小遍历
                    if p<_bid_max_level_price:
                        _bid_max_level_price = p
                        _bid_max_level_qty = l.qty
                        break
            else:
                snap_bid_levels[nb] = price_level(0,0)

        return snap_ask_levels, snap_bid_levels

    def _chkSnapTimestamp(self, se_timestamp, my_timestamp):
        '''
        检查交易所快照和本地重建快照的时戳是否符合：
        深交所本地时戳的秒应小于等交易所快照时戳
        '''

        if self.SecurityIDSource==SecurityIDSource_SZSE:
            return my_timestamp//1000 <= se_timestamp//1000 +1
        elif self.SecurityIDSource==SecurityIDSource_SSE:
            return False    #TODO: [Low Priority]
        else:
            return False

    def are_you_ok(self):
        im_ok = True
        if len(self.market_snaps):
            self.ERR(f'unmatched market snap size={len(self.market_snaps)}:')
            for s in self.market_snaps:
                self.ERR(f'#{s._seq}')
            im_ok = False
        return im_ok

    def save(self):
        '''save/load 用于保存/加载测试时刻'''
        data = {}
        for attr in self.__slots__:
            if attr in ['logger', 'DBG', 'INFO', 'WARN', 'ERR']:
                continue

            value = getattr(self, attr)
            if attr == 'order_map' or attr == 'bid_level_tree' or attr == 'ask_level_tree':
                data[attr] = {}
                for i in value:
                    data[attr][i] = value[i].save()
            elif attr == 'rebuilt_snaps' or attr == 'market_snaps':
                data[attr] = [x.save() for x in value]
            elif attr == 'last_snap':
                data[attr] = value.save()
            else:
                data[attr] = value
        return data

    def load(self, data):
        setattr(self, 'instrument_type', data['instrument_type'])
        for attr in self.__slots__:
            if attr in ['logger', 'DBG', 'INFO', 'WARN', 'ERR']:
                continue

            if attr == 'order_map':
                v = {}
                for i in data[attr]:
                    v[i] = ob_order(axsbe_order(), INSTRUMENT_TYPE.UNKNOWN)
                    v[i].load(data[attr][i])
                setattr(self, attr, v)
            elif attr == 'bid_level_tree' or attr == 'ask_level_tree':
                v = {}
                for i in data[attr]:
                    v[i] = level_node(-1, -1, -1)
                    v[i].load(data[attr][i])
                setattr(self, attr, v)
            elif attr == 'rebuilt_snaps' or attr == 'market_snaps':
                v = []
                for d in data[attr]:
                    if self.instrument_type==INSTRUMENT_TYPE.STOCK:
                        s = axsbe_snap_stock()
                    else:
                        raise f'unable to load instrument_type={self.instrument_type}'
                    s.load(d)
                    v.append(s)
                setattr(self, attr, v)
            elif attr == 'last_snap':
                if self.instrument_type==INSTRUMENT_TYPE.STOCK:
                    v = axsbe_snap_stock()
                else:
                    raise f'unable to load instrument_type={self.instrument_type}'
                v.load(data[attr])
                setattr(self, attr, v)
            else:
                setattr(self, attr, data[attr])
        ## 日志
        self.logger = logging.getLogger(f'{self.SecurityID:06d}')
        g_logger = logging.getLogger('main')
        self.logger.setLevel(g_logger.getEffectiveLevel())
        for h in g_logger.handlers:
            self.logger.addHandler(h)
            axob_logger.addHandler(h) #这里补上模块日志的handler，有点ugly TODO: better way [low prioryty]

        self.DBG = self.logger.debug
        self.INFO = self.logger.info
        self.WARN = self.logger.warning
        self.ERR = self.logger.error
