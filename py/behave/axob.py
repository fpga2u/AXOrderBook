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

from tool.msg_util import axsbe_base, axsbe_exe, axsbe_order, axsbe_snap, price_level

class AXOB():
    def __init__(self, SecurityID:int):
        self.SecurityID = SecurityID

        ## 结构数据
        self.order_map = {}
        self.bid_level_tree = {}
        self.ask_level_tree = {}

        ## 检查

    def onMsg(self, msg):
        if isinstance(msg, axsbe_order) or isinstance(msg, axsbe_exe) or isinstance(msg, axsbe_snap):
            if msg.SecurityID!=self.SecurityID:
                return

            if isinstance(msg, axsbe_order):
                self.onOrder(msg)
            elif isinstance(msg, axsbe_exe):
                self.onExec(msg)
            else:# isinstance(msg, axsbe_snap):
                self.onSnap(msg)
        else:
            return
