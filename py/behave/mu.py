# -*- coding: utf-8 -*-

from behave.axob import AXOB, AX_SIGNAL
from tool.axsbe_base import TPM, SecurityIDSource_SSE, SecurityIDSource_SZSE
from tool.msg_util import *

import logging

class MU():
    '''
    管理多个AXOB
    行为包含了FPGA的MU和前级arbiter的动作:
      FPGA的AB:分发消息给MU
      FPGA的MU:交易阶段管理【使MU接口符合统一格式，与AB解耦，AB可能由RTL实现。】【MU内部的消息格式重构需要放在最前端，可能要移到AB。】
    '''
    __slots__ = [
        'axobs',

        'SecurityIDSource', 

        'channel_map',

        'msg_nb',

        # profile
        'pf_order_map_maxSize',
        'pf_level_tree_maxSize',
        'pf_bid_level_tree_maxSize',
        'pf_ask_level_tree_maxSize',
        'pf_AskWeightSize_max',
        'pf_AskWeightValue_max',
        'pf_BidWeightSize_max',
        'pf_BidWeightValue_max',

        'logger',
        'DBG',
        'INFO',
        'WARN',
        'ERR',
    ]
    def __init__(self, SecurityID_list, SecurityIDSource, instrument_type:INSTRUMENT_TYPE, load_data=None) -> None:
        if load_data is not None:
            self.load(load_data)
        else:
            self.axobs = dict(zip(SecurityID_list, [AXOB(x, SecurityIDSource, instrument_type) for x in SecurityID_list]))

            self.SecurityIDSource = SecurityIDSource

            self.channel_map ={}  #按不同ChannelID分组标的: ChannelID : {'TPM':?, 'SecurityID_list':[] }
                                  #在FPGA实现时，开盘前：FPGA先报告ChannelID、新股SecID；
                                  #             host将ChannelID相同的分到一个MU，新股按最大成交量分配。

            # for test
            self.msg_nb = 0
            self.pf_order_map_maxSize = 0
            self.pf_level_tree_maxSize = 0
            self.pf_bid_level_tree_maxSize = 0
            self.pf_ask_level_tree_maxSize = 0
            self.pf_AskWeightSize_max = 0
            self.pf_AskWeightValue_max = 0
            self.pf_BidWeightSize_max = 0
            self.pf_BidWeightValue_max = 0
            
            # for debug
            self.logger = logging.getLogger(f'mu-{SecurityID_list[0]:06d}...')
            g_logger = logging.getLogger('main')
            self.logger.setLevel(g_logger.getEffectiveLevel())
            for h in g_logger.handlers:
                self.logger.addHandler(h)

            self.DBG = self.logger.debug
            self.INFO = self.logger.info
            self.WARN = self.logger.warning
            self.ERR = self.logger.error
        self.INFO(f'SecurityID_list={SecurityID_list}')

    def unique_ChannelNo(self, msg):
        # 将逐笔和快照的ChannelNo统一，用于管理分组
        if self.SecurityIDSource==SecurityIDSource_SZSE:
            # 深交所 逐笔和快照的ChannelNo相差1000
            if isinstance(msg, (axsbe_order, axsbe_exe)):
                return msg.ChannelNo - 2000
            elif isinstance(msg, axsbe_snap_stock):
                return msg.ChannelNo - 1000
            else:
                return 0
        elif self.SecurityIDSource==SecurityIDSource_SSE:
            # 上交所 快照ChannelNo为0，无法和逐笔对应起来，按照只有1个channle来处理
            return 0
        else:
            return 0

    def onMsg(self, msg):
        '''
        交易阶段管理
        '''
        unique_ChannelNo = self.unique_ChannelNo(msg)
        
        if unique_ChannelNo not in self.channel_map:
            self.channel_map[unique_ChannelNo] = {
                'TPM':TPM.Starting,
                'SecurityID_list':[],
            }
        if msg.SecurityID in self.axobs and msg.SecurityID not in self.channel_map[unique_ChannelNo]['SecurityID_list']:
            self.channel_map[unique_ChannelNo]['SecurityID_list'].append(msg.SecurityID)
        
        if len(self.channel_map[unique_ChannelNo]['SecurityID_list']):
            if self.channel_map[unique_ChannelNo]['TPM']==TPM.Starting: # Starting -> OpenCall
                #深交所：任意逐笔，或快照时戳大于等于开盘或快照状态（TODO:回归测试）
                #上交所：逐笔要等到9:25才发送，仅用快照时戳或快照状态
                if (isinstance(msg, (axsbe_order, axsbe_exe))) or\
                   (isinstance(msg, axsbe_status) and msg.TradingPhaseMarket==TPM.OpenCall) or\
                   (isinstance(msg, axsbe_snap_stock) and (msg.HHMMSSms>=91500000 or msg.TradingPhaseMarket==TPM.OpenCall)):
                    self.INFO(f'Chnl {unique_ChannelNo} Starting -> OpenCall')
                    self.channel_map[unique_ChannelNo]['TPM'] = TPM.OpenCall
                    for id in self.channel_map[unique_ChannelNo]['SecurityID_list']: self.axobs[id].onMsg(AX_SIGNAL.OPENCALL_BGN)
            elif self.channel_map[unique_ChannelNo]['TPM']==TPM.OpenCall: # OpenCall -> PreTradingBreaking
                # 任意逐笔离开开盘集合竞价，或快照时戳超过盘前休市15s
                # 上交所: 债券市场状态进入连续自动撮合
                if (isinstance(msg, axsbe_exe) and msg.TradingPhaseMarket==TPM.PreTradingBreaking) or\
                   (isinstance(msg, axsbe_status) and msg.TradingPhaseMarket==TPM.ContinuousAutomaticMatching) or\
                   (isinstance(msg, axsbe_snap_stock) and msg.HHMMSSms>=92515000):
                    self.INFO(f'Chnl {unique_ChannelNo} OpenCall -> PreTradingBreaking')
                    self.channel_map[unique_ChannelNo]['TPM'] = TPM.PreTradingBreaking
                    for id in self.channel_map[unique_ChannelNo]['SecurityID_list']: self.axobs[id].onMsg(AX_SIGNAL.OPENCALL_END)
            elif self.channel_map[unique_ChannelNo]['TPM']==TPM.PreTradingBreaking: # PreTradingBreaking -> AMTrading
                #任意逐笔进入上午连续竞价阶段，或快照时戳大于等于上午连续竞价
                if (isinstance(msg, (axsbe_order, axsbe_exe)) and msg.TradingPhaseMarket==TPM.AMTrading) or\
                   (isinstance(msg, axsbe_snap_stock) and msg.HHMMSSms>=93000000):
                    self.INFO(f'Chnl {unique_ChannelNo} PreTradingBreaking -> AMTrading')
                    self.channel_map[unique_ChannelNo]['TPM'] = TPM.AMTrading
                    for id in self.channel_map[unique_ChannelNo]['SecurityID_list']: self.axobs[id].onMsg(AX_SIGNAL.AMTRADING_BGN)
            elif self.channel_map[unique_ChannelNo]['TPM']==TPM.AMTrading: # AMTrading -> Breaking
                #快照时戳大于等于中午休市15s
                if (isinstance(msg, axsbe_snap_stock) and msg.HHMMSSms>=113015000):
                    self.INFO(f'Chnl {unique_ChannelNo} AMTrading -> Breaking')
                    self.channel_map[unique_ChannelNo]['TPM'] = TPM.Breaking
                    for id in self.channel_map[unique_ChannelNo]['SecurityID_list']: self.axobs[id].onMsg(AX_SIGNAL.AMTRADING_END)
            elif self.channel_map[unique_ChannelNo]['TPM']==TPM.Breaking: # Breaking -> PMTrading
                #任意逐笔，或快照时戳大于等于下午连续竞价
                if (isinstance(msg, (axsbe_order, axsbe_exe))) or\
                   (isinstance(msg, axsbe_snap_stock) and msg.HHMMSSms>=130000000):
                    self.INFO(f'Chnl {unique_ChannelNo} Breaking -> PMTrading')
                    self.channel_map[unique_ChannelNo]['TPM'] = TPM.PMTrading
                    for id in self.channel_map[unique_ChannelNo]['SecurityID_list']: self.axobs[id].onMsg(AX_SIGNAL.PMTRADING_BGN)
            elif self.channel_map[unique_ChannelNo]['TPM']==TPM.PMTrading: # PMTrading -> CloseCall
                #任意逐笔进入收盘集合竞价阶段，或快照时戳大于等于收盘集合竞价15s
                if (isinstance(msg, (axsbe_order, axsbe_exe)) and msg.TradingPhaseMarket==TPM.CloseCall) or\
                   (isinstance(msg, axsbe_snap_stock) and msg.HHMMSSms>=145715000):
                    self.INFO(f'Chnl {unique_ChannelNo} PMTrading -> CloseCall')
                    self.channel_map[unique_ChannelNo]['TPM'] = TPM.CloseCall
                    for id in self.channel_map[unique_ChannelNo]['SecurityID_list']: self.axobs[id].onMsg(AX_SIGNAL.PMTRADING_END)
            elif self.channel_map[unique_ChannelNo]['TPM']==TPM.CloseCall: # CloseCall -> Ending
                #任意成交离开收盘集合竞价阶段，或快照时戳大于等于闭市15s
                # 上交所: 债券市场状态进入闭市=15:00:00~15:04:59
                if (isinstance(msg, axsbe_exe) and msg.TradingPhaseMarket==TPM.Ending) or\
                   (isinstance(msg, axsbe_status) and msg.TradingPhaseMarket==TPM.Closing) or\
                   (isinstance(msg, axsbe_snap_stock) and msg.HHMMSSms>=150015000):
                    self.INFO(f'Chnl {unique_ChannelNo} CloseCall -> Ending')
                    self.channel_map[unique_ChannelNo]['TPM'] = TPM.Ending
                    for id in self.channel_map[unique_ChannelNo]['SecurityID_list']: self.axobs[id].onMsg(AX_SIGNAL.ALL_END)
        else:
            return

        if msg.SecurityID not in self.axobs:
            return

        # TODO: 重构消息给axob？
        self.axobs[msg.SecurityID].onMsg(msg)

        self.msg_nb += 1
        self.profile()

    def are_you_ok(self):
        ok_nb = 0
        ng_list = []
        for id, x in self.axobs.items():
            if isTPMfreeze(x):
                ok = x.are_you_ok()
                if not ok:
                    ng_list.append(id)
                ok_nb += ok
            else:
                ok_nb += 1
        if len(ng_list):
            self.ERR(f'ng nb={len(ng_list)}')
            self.ERR(f'ng_list={ng_list}')
        return len(ng_list)==0

    @property
    def TradingPhaseMarket(self):
        ret = TPM.Starting
        for ch in self.channel_map:
            t = self.channel_map[ch]['TPM']
            if t<=TPM.Ending:
                ret = max(ret, t) #取最晚的TPM
        return ret

    def profile(self):
        k = [x.order_map_size for _, x in self.axobs.items()]
        k = sum(k)
        if k>self.pf_order_map_maxSize:self.pf_order_map_maxSize=k

        k = [x.level_tree_size for _, x in self.axobs.items()]
        k = sum(k)
        if k>self.pf_level_tree_maxSize:self.pf_level_tree_maxSize=k

        k = [x.bid_level_tree_size for _, x in self.axobs.items()]
        k = sum(k)
        if k>self.pf_bid_level_tree_maxSize:self.pf_bid_level_tree_maxSize=k

        k = [x.ask_level_tree_size for _, x in self.axobs.items()]
        k = sum(k)
        if k>self.pf_ask_level_tree_maxSize:self.pf_ask_level_tree_maxSize=k

        k = [x.pf_AskWeightSize_max for _, x in self.axobs.items()]
        k = max(k)
        if k>self.pf_AskWeightSize_max:self.pf_AskWeightSize_max=k
        k = [x.pf_AskWeightValue_max for _, x in self.axobs.items()]
        k = max(k)
        if k>self.pf_AskWeightValue_max:self.pf_AskWeightValue_max=k
        
        k = [x.pf_BidWeightSize_max for _, x in self.axobs.items()]
        k = max(k)
        if k>self.pf_BidWeightSize_max:self.pf_BidWeightSize_max=k
        k = [x.pf_BidWeightValue_max for _, x in self.axobs.items()]
        k = max(k)
        if k>self.pf_BidWeightValue_max:self.pf_BidWeightValue_max=k

    def __str__(self) -> str:
        s = '========================\n'
        for _, x in self.axobs.items():
            s += str(x)
            s += '--------\n'
        s+= '========================\n'
        s+= f'  MU-{len(self.axobs)}.MUpf_order_map_maxSize={self.pf_order_map_maxSize}({bitSizeOf(self.pf_order_map_maxSize)}b)\n'
        s+= f'  MU-{len(self.axobs)}.MUpf_level_tree_maxSize={self.pf_level_tree_maxSize}({bitSizeOf(self.pf_level_tree_maxSize)}b)\n'
        s+= f'  MU-{len(self.axobs)}.MUpf_bid_level_tree_maxSize={self.pf_bid_level_tree_maxSize}({bitSizeOf(self.pf_bid_level_tree_maxSize)}b) MU-{len(self.axobs)}.MUpf_ask_level_tree_maxSize={self.pf_ask_level_tree_maxSize}({bitSizeOf(self.pf_ask_level_tree_maxSize)}b)\n'
        s+= f'  MU-{len(self.axobs)}.MUpf_AskWeightSize_max={self.pf_AskWeightSize_max}({bitSizeOf(self.pf_AskWeightSize_max)}b)\n'
        s+= f'  MU-{len(self.axobs)}.MUpf_AskWeightValue_max={self.pf_AskWeightValue_max}({bitSizeOf(self.pf_AskWeightValue_max)}b)\n'
        s+= f'  MU-{len(self.axobs)}.MUpf_BidWeightSize_max={self.pf_BidWeightSize_max}({bitSizeOf(self.pf_BidWeightSize_max)}b)\n'
        s+= f'  MU-{len(self.axobs)}.MUpf_BidWeightValue_max={self.pf_BidWeightValue_max}({bitSizeOf(self.pf_BidWeightValue_max)}b)\n'

        return s

    def save(self):
        '''save/load 用于保存/加载测试时刻'''
        data = {}
        for attr in self.__slots__:
            if attr in ['logger', 'DBG', 'INFO', 'WARN', 'ERR']:
                continue

            value = getattr(self, attr)
            if attr in ['axobs']:
                data[attr] = {}
                for i in value:
                    data[attr][i] = value[i].save()
            else:
                data[attr] = value
        return data

    def load(self, data):
        for attr in self.__slots__:
            if attr in ['logger', 'DBG', 'INFO', 'WARN', 'ERR']:
                continue

            if attr in ['axobs']:
                v = {}
                for i in data[attr]:
                    v[i] = AXOB(-1, -1, INSTRUMENT_TYPE.UNKNOWN, load_data=data[attr][i])
                setattr(self, attr, v)
            else:
                setattr(self, attr, data[attr])
        ## 日志
        SecurityID_list = list(data['axobs'].keys())
        self.logger = logging.getLogger(f'mu-{SecurityID_list[0]:06d}...')
        g_logger = logging.getLogger('main')
        self.logger.setLevel(g_logger.getEffectiveLevel())
        for h in g_logger.handlers:
            self.logger.addHandler(h)

        self.DBG = self.logger.debug
        self.INFO = self.logger.info
        self.WARN = self.logger.warning
        self.ERR = self.logger.error
