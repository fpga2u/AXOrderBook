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

SIDE_BID = 0
SIDE_ASK = 1

TYPE_LIMIT  = 0   #限价
TYPE_MARKET = 1   #市价
TYPE_SIDE   = 2   #本方最优

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

        self.qty = order.OrderQty    # 上海 3位小数

        if order.Side_str=='买入':
            self.side = SIDE_BID
        elif order.Side_str=='卖出':
            self.side = SIDE_ASK
        else:   #TODO: 映射上海
            axob_logger.error(f'order ApplSeqNum={order.ApplSeqNum} side={order.Side}({order.Side_str}) unknown!')

        if order.Type_str=='限价':
            self.type = TYPE_LIMIT
        elif order.Type_str=='市价':
            self.type = TYPE_MARKET
        elif order.Type_str=='本方最优':
            self.type = TYPE_SIDE
        else:   #TODO: 映射上海
            axob_logger.error(f'order ApplSeqNum={order.ApplSeqNum} type={order.OrdType}({order.Type_str}) unknown!')

        ## 位宽及精度舍入可行性检查
        if self.applSeqNum >= (1<<APPSEQ_BIT_SIZE):
            axob_logger.error(f'order ApplSeqNum={order.ApplSeqNum} ovf!')

        if self.price >= (1<<PRICE_BIT_SIZE):
            axob_logger.error(f'order ApplSeqNum={order.ApplSeqNum} Price={order.Price} ovf!')

        if self.qty >= (1<<QTY_BIT_SIZE):
            axob_logger.error(f'order ApplSeqNum={order.ApplSeqNum} Volumn={order.OrderQty} ovf!')

        if order.SecurityIDSource==SecurityIDSource_SZSE:
            if instrument_type==INSTRUMENT_TYPE.STOCK and order.Price % SZSE_STOCK_PRICE_RD:
                axob_logger.error(f'order SZSE STOCK ApplSeqNum={order.ApplSeqNum} Price={order.Price} precision dnf!')
            elif instrument_type==INSTRUMENT_TYPE.FUND and order.Price % SZSE_FUND_PRICE_RD:
                axob_logger.error(f'order SZSE FUND ApplSeqNum={order.ApplSeqNum} Price={order.Price} precision dnf!')
        elif order.SecurityIDSource==SecurityIDSource_SSE:
            if instrument_type==INSTRUMENT_TYPE.STOCK and order.Price % SSE_STOCK_PRICE_RD:
                axob_logger.error(f'order SSE STOCK ApplSeqNum={order.ApplSeqNum} Price={order.Price} precision dnf!')

class AXOB():
    def __init__(self, SecurityID:int, instrument_type:INSTRUMENT_TYPE):
        self.SecurityID = SecurityID
        self.instrument_type = instrument_type

        ## 结构数据
        self.order_map = {}
        self.bid_level_tree = {}
        self.ask_level_tree = {}

        self.bid_best_level = None
        self.ask_best_level = None

        ## 检查

        ##
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
        else:
            return

    def onOrder(self, order:axsbe_order):
        '''
        逐笔订单入口
        需要注意的是价格精度
        '''
        self.DBG(f'onOrder:{order}')
        _order = ob_order(order, self.instrument_type)
        if _order.type==TYPE_LIMIT:
            pass
        else:
            # 市价单，都必须在开盘之后
            if self.bid_best_level is None and self.ask_best_level is None:
                self.ERR('未定义模式:市价单早于价格档')
            if order.Type_str=='市价':
                # 市价单，几种可能：
                #    * 对手方最优价格申报：最后挂在对方一档或者二档
                #    * 最优五档即时成交剩余撤销申报：最后撤单
                #    * 即时成交剩余撤销申报：最后撤单
                #    * 全额成交或撤销申报：最后撤单
                pass
            else:
                # 本方最优价格申报 
                pass
