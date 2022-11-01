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
from tool.msg_util import axsbe_base, axsbe_exe, axsbe_order, axsbe_snap_stock, price_level
import tool.msg_util as msg_util
from tool.axsbe_base import SecurityIDSource_SSE, SecurityIDSource_SZSE

axob_logger = logging.getLogger(__name__)

class INSTRUMENT_TYPE(Enum):
    STOCK  = 0   #股票
    FUND   = 1   #基金
    KZZ    = 2   #可转债
    OPTION = 3   #期权
    BOND   = 4   #债券
    NHG    = 5   #逆回购

APPSEQ_BIT_SIZE = 34    # 序列号，34b，约170亿
PRICE_BIT_SIZE  = 20    # 价格，20b，1048575，股票:10485.75;基金:1048.575。（若统一到3位小数则考虑用24b，则只需深圳//10）
QTY_BIT_SIZE    = 30    # 数量，30b，(1,073,741,823)，深圳2位小数，上海3位小数

STOCK_PRICE_PRECISION = 100  # 股票价格精度：2位小数，(深圳原始数据4位，上海3位)
FUND_PRICE_PRECISION  = 1000 # 基金价格精度：3位小数，(深圳原始数据4位，上海3位)

# 
QTY_PRECISION_SZSE   = 100   # 数量精度：深圳2位小数
QTY_PRECISION_SSE    = 1000  # 数量精度：上海3位小数

class SIDE(Enum):
    BID = 0
    ASK = 1

class TYPE(Enum):
    LIMIT  = 0   #限价
    MARKET = 1   #市价
    SIDE   = 2   #本方最优

# 用于将原始精度转换到ob精度
SZSE_STOCK_PRICE_RD = msg_util.SZSE_PRECISION_PRICE // STOCK_PRICE_PRECISION
SZSE_FUND_PRICE_RD = msg_util.SZSE_PRECISION_PRICE // FUND_PRICE_PRECISION
SSE_STOCK_PRICE_RD = msg_util.SSE_PRECISION_PRICE // STOCK_PRICE_PRECISION
# SSE_FUND_PRICE_RES = msg_util.SSE_PRECISION_PRICE // FUND_PRICE_PRECISION TODO:确认精度

class ob_order():
    '''专注于内部使用的字段格式与位宽'''
    def __init__(self, order:axsbe_order, instrument_type:INSTRUMENT_TYPE):
        self.securityID = order.SecurityID
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
            axob_logger.error(f'order ApplSeqNum={order.ApplSeqNum} SecurityIDSource={order.SecurityIDSource} unknown!')
        self.traded = False #仅用于市价单，当有成交后，市价单的价格将确定

        self.qty = order.OrderQty    # 上海 3位小数

        if order.Side_str=='买入':
            self.side = SIDE.BID
        elif order.Side_str=='卖出':
            self.side = SIDE.ASK
        else:   #TODO: 映射上海
            axob_logger.error(f'order ApplSeqNum={order.ApplSeqNum} side={order.Side}({order.Side_str}) unknown!')

        if order.Type_str=='限价':
            self.type = TYPE.LIMIT
        elif order.Type_str=='市价':
            self.type = TYPE.MARKET
        elif order.Type_str=='本方最优':
            self.type = TYPE.SIDE
        else:   #TODO: 映射上海
            axob_logger.error(f'order ApplSeqNum={order.ApplSeqNum} type={order.OrdType}({order.Type_str}) unknown!')

        ## 位宽及精度舍入可行性检查
        if self.applSeqNum >= (1<<APPSEQ_BIT_SIZE):
            axob_logger.error(f'order ApplSeqNum={order.ApplSeqNum} ovf!')

        if self.price >= (1<<PRICE_BIT_SIZE):
            axob_logger.error(f'order ApplSeqNum={order.ApplSeqNum} Price={order.Price} ovf!')

        if self.qty >= (1<<QTY_BIT_SIZE):
            axob_logger.error(f'order ApplSeqNum={order.ApplSeqNum} Volumn={order.OrderQty} ovf!')

        if self.type==TYPE.LIMIT:   #检查限价单价格是否溢出；市价单价格是无效值，不可参与检查
            if order.SecurityIDSource==SecurityIDSource_SZSE:
                if instrument_type==INSTRUMENT_TYPE.STOCK and order.Price % SZSE_STOCK_PRICE_RD:
                    axob_logger.error(f'order SZSE STOCK ApplSeqNum={order.ApplSeqNum} Price={order.Price} precision dnf!')
                elif instrument_type==INSTRUMENT_TYPE.FUND and order.Price % SZSE_FUND_PRICE_RD:
                    axob_logger.error(f'order SZSE FUND ApplSeqNum={order.ApplSeqNum} Price={order.Price} precision dnf!')
            elif order.SecurityIDSource==SecurityIDSource_SSE:
                if instrument_type==INSTRUMENT_TYPE.STOCK and order.Price % SSE_STOCK_PRICE_RD:
                    axob_logger.error(f'order SSE STOCK ApplSeqNum={order.ApplSeqNum} Price={order.Price} precision dnf!')

    def __str__(self) -> str:
        return f'{self.applSeqNum}'

class level_node():
    def __init__(self, price, qty):
        self.price = price
        self.qty = qty


class AXOB():
    def __init__(self, SecurityID:int, instrument_type:INSTRUMENT_TYPE, DnLimitPx, UpLimitPx):
        self.SecurityID = SecurityID
        self.instrument_type = instrument_type

        ## 结构数据
        self.order_map = {} #订单队列，以applSeqNum作为索引
        self.bid_level_tree = {} #买方价格档，以价格作为索引
        self.ask_level_tree = {} #卖方价格档

        self.bid_best_level_price = 0
        self.bid_best_level_qty = 0
        self.ask_best_level_price = 0
        self.ask_best_level_qty = 0

        self.DnLimitPx = DnLimitPx  #TODO: cover: 无涨跌停价
        self.UpLimitPx = UpLimitPx  #TODO: cover: 无涨跌停价
        
        self.BidWeightSize = 0
        self.BidWeightValue = 0
        self.AskWeightSize = 0
        self.AskWeightValue = 0

        self.holding_order = None
        self.holding_nb = 0

        ## 检查
        self.last_msg_timestamp = 0
        self.lob_snaps = []

        ## 日志
        self.logger = logging.getLogger(f'{self.SecurityID:06d}')
        self.DBG = self.logger.debug
        self.INFO = self.logger.info
        self.WARN = self.logger.warning
        self.ERR = self.logger.error

    def onMsg(self, msg):
        '''处理总入口'''
        if isinstance(msg, axsbe_order) or isinstance(msg, axsbe_exe) or isinstance(msg, axsbe_snap_stock):
            if msg.SecurityID!=self.SecurityID:
                return

            if isinstance(msg, axsbe_order):
                self.onOrder(msg)
            elif isinstance(msg, axsbe_exe):
                self.onExec(msg)
            else:# isinstance(msg, axsbe_snap_stock):
                self.onSnap(msg)

            ## 仅用于检查
            self.last_msg_timestamp = msg.TransactTime

        else:
            return

    def onOrder(self, order:axsbe_order):
        '''
        逐笔订单入口，限价单、市价单分开处理
        '''
        self.DBG(f'onOrder:{order}')
        _order = ob_order(order, self.instrument_type)
        if _order.type==TYPE.MARKET:
            # 市价单，都必须在开盘之后
            if self.bid_best_level_qty==0 and self.ask_best_level_qty==0:
                self.ERR('未定义模式:市价单早于价格档') #TODO: cover
            #if _order.type==TYPE.MARKET:
                # 市价单，几种可能：
                #    * 对手方最优价格申报：有成交、最后挂在对方一档或者二档
                #    * 最优五档即时成交剩余撤销申报：最后有撤单
                #    * 即时成交剩余撤销申报：最后有撤单
                #    * 全额成交或撤销申报：最后有撤单
            if _order.type==TYPE.SIDE:
                # 本方最优价格申报 转限价单
                if _order.side==SIDE.BID:
                    if self.bid_best_level_price!=0 and self.bid_best_level_qty!=0:   #本方有量
                        _order.price = self.bid_best_level_price
                    else:
                        _order.price = self.DnLimitPx
                        axob_logger.error(f'order #{_order.applSeqNum} 本方最优买单 但无本方价格!') #TODO: cover
                else:
                    if self.ask_best_level_price!=0 and self.ask_best_level_qty!=0:   #本方有量
                        _order.price = self.ask_best_level_price
                    else:
                        _order.price = self.UpLimitPx
                        axob_logger.error(f'order #{_order.applSeqNum} 本方最优卖单 但无本方价格!') #TODO: cover
        self.onLimitOrder(_order)

    def onLimitOrder(self, order:ob_order):
        if order.tradingPhase == axsbe_base.TPM.OpenCall or order.tradingPhase == axsbe_base.TPM.CloseCall: #集合竞价期间，直接插入
            self.insertOrder(order)
        else:
            #把此前缓存的订单(市价/限价)插入LOB
            if self.holding_nb != 0:
                if self.holding_order.type == TYPE.MARKET and not self.holding_order.traded:
                    self.ERR(f'市价单 {self.holding_order} 未伴随成交')

                self.insertOrder(self.holding_order)
                self.holding_nb = 0

                snap = self.genSnap()   #先出一个snap

                ## 仅用于检查
                self.DBG(snap)
                self.lob_snaps.append(snap)

            #若是可能成交的限价单，则缓存住，等成交
            if (order.side == SIDE.BID and (order.price >= self.bid_best_level_price and self.bid_best_level_qty > 0)) or \
               (order.side == SIDE.ASK and (order.price <= self.ask_best_level_price and self.ask_best_level_qty > 0)):
                self.holding_order = order
                self.holding_nb += 1
            else:
                self.insertOrder(order)

                snap = self.genSnap()   #再出一个snap

                ## 仅用于检查
                self.DBG(snap)
                self.lob_snaps.append(snap)

    def insertOrder(self, order:ob_order):
        '''
        订单入列，更新对应的价格档位数据
        '''
        self.order_map[order.applSeqNum] = order
        
        if order.side == SIDE.BID:
            # self.bidPriceCacheHandler.addQty(order.price, order.qty)
            if order.price in self.bid_level_tree:
                self.bid_level_tree[order.price].qty += order.qty
            else:
                node = level_node(order.price, order.qty)
                self.bid_level_tree[order.price] = node

                if self.bid_best_level_price==0 or node.price > self.bid_best_level_price:  #买方出现更高价格
                    self.bid_best_level_price = order.price
                    self.bid_best_level_qty = order.qty

            self.BidWeightSize += order.qty
            self.BidWeightValue += order.price * order.qty
        elif order.side == SIDE.ASK:
            # self.askPriceCacheHandler.addQty(order.price, order.qty)
            if order.price in self.ask_level_tree:
                self.ask_level_tree[order.price].qty += order.qty
            else:
                node = level_node(order.price, order.qty)
                self.ask_level_tree[order.price] = node

                if self.ask_best_level_price==0 or node.price < self.ask_best_level_price: #卖方出现更低价格
                    self.ask_best_level_price = order.price
                    self.ask_best_level_qty = order.qty

            self.AskWeightSize += order.qty
            self.AskWeightValue += order.price * order.qty

    def onExec(self, exec:axsbe_exe):
        pass
    def onSnap(self, snap):
        pass
    def genSnap(self):
        pass