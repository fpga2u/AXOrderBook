# -*- coding: utf-8 -*-

from behave.axob import AXOB, AX_SIGNAL
from tool.axsbe_base import TPM
from tool.msg_util import *


class MU():
    def __init__(self, SecurityID_list, SecurityIDSource, instrument_type:INSTRUMENT_TYPE ) -> None:
        self.TradingPhaseMarket = TPM.Starting
        self.axobs = dict(zip(SecurityID_list, [AXOB(x, SecurityIDSource, instrument_type) for x in SecurityID_list]))

    def onMsg(self, msg):
        '''
        交易阶段管理
        TODO: 波动性中断
        '''
        
        if self.TradingPhaseMarket==TPM.Starting: # Starting -> OpenCall
            #任意逐笔，或快照时戳大于等于开盘
            if (isinstance(msg, (axsbe_order, axsbe_exe))) or\
               (isinstance(msg, axsbe_snap_stock) and msg.HHMMSSms>=91500000):
                self.TradingPhaseMarket = TPM.OpenCall
                for _, ob in self.axobs.items():ob.onMsg(AX_SIGNAL.OPENCALL_BGN)
        elif self.TradingPhaseMarket==TPM.OpenCall: # OpenCall -> PreTradingBreaking
            # 任意逐笔离开开盘集合竞价，或快照时戳超过盘前休市15s
            if (isinstance(msg, axsbe_exe) and msg.TradingPhaseMarket==TPM.PreTradingBreaking) or\
               (isinstance(msg, axsbe_snap_stock) and msg.HHMMSSms>=92515000):
                self.TradingPhaseMarket = TPM.PreTradingBreaking
                for _, ob in self.axobs.items():ob.onMsg(AX_SIGNAL.OPENCALL_END)
        elif self.TradingPhaseMarket==TPM.PreTradingBreaking: # PreTradingBreaking -> AMTrading
            #任意逐笔进入上午连续竞价阶段，或快照时戳大于等于上午连续竞价
            if (isinstance(msg, (axsbe_order, axsbe_exe)) and msg.TradingPhaseMarket==TPM.AMTrading) or\
               (isinstance(msg, axsbe_snap_stock) and msg.HHMMSSms>=93000000):
                self.TradingPhaseMarket = TPM.AMTrading
                for _, ob in self.axobs.items():ob.onMsg(AX_SIGNAL.AMTRADING_BGN)
        elif self.TradingPhaseMarket==TPM.AMTrading: # AMTrading -> Breaking
            #快照时戳大于等于中午休市15s
            if (isinstance(msg, axsbe_snap_stock) and msg.HHMMSSms>=113015000):
                self.TradingPhaseMarket = TPM.Breaking
                for _, ob in self.axobs.items():ob.onMsg(AX_SIGNAL.AMTRADING_END)
        elif self.TradingPhaseMarket==TPM.Breaking: # Breaking -> PMTrading
            #任意逐笔，或快照时戳大于等于下午连续竞价
            if (isinstance(msg, (axsbe_order, axsbe_exe))) or\
               (isinstance(msg, axsbe_snap_stock) and msg.HHMMSSms>=130000000):
                self.TradingPhaseMarket = TPM.PMTrading
                for _, ob in self.axobs.items():ob.onMsg(AX_SIGNAL.PMTRADING_BGN)
        elif self.TradingPhaseMarket==TPM.PMTrading: # PMTrading -> CloseCall
            #任意逐笔进入收盘集合竞价阶段，或快照时戳大于等于收盘集合竞价15s
            if (isinstance(msg, (axsbe_order, axsbe_exe)) and msg.TradingPhaseMarket==TPM.CloseCall) or\
               (isinstance(msg, axsbe_snap_stock) and msg.HHMMSSms>=145715000):
                self.TradingPhaseMarket = TPM.CloseCall
                for _, ob in self.axobs.items():ob.onMsg(AX_SIGNAL.PMTRADING_END)
        elif self.TradingPhaseMarket==TPM.CloseCall: # PMTrading -> CloseCall
            #任意成交离开收盘集合竞价阶段，或快照时戳大于等于闭市15s
            if (isinstance(msg, axsbe_exe) and msg.TradingPhaseMarket==TPM.Ending) or\
               (isinstance(msg, axsbe_snap_stock) and msg.HHMMSSms>=150015000):
                self.TradingPhaseMarket = TPM.Ending
                for _, ob in self.axobs.items():ob.onMsg(AX_SIGNAL.ALL_END)

        if msg.SecurityID not in self.axobs:
            return

        self.axobs[msg.SecurityID].onMsg(msg)

    def are_you_ok(self):
        ok_nb = 0
        for _, x in self.axobs.items():
            if isTPMfreeze(x):
                ok_nb += x.are_you_ok()
            else:
                ok_nb += 1
        return ok_nb==len(self.axobs)