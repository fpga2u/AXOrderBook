# -*- coding: utf-8 -*-

import tool.axsbe_base as axsbe_base
from tool.axsbe_base import TPI, TPM
import struct


class axsbe_status(axsbe_base.axsbe_base):
    '''
    深交所:心跳
    上交所:心跳、债券逐笔合并流市场状态
    '''
    
    __slots__ = [
        'SecurityIDSource',
        'MsgType',
        'SecurityID',
        'ChannelNo',
        'ApplSeqNum',
        'TradingPhaseInstrument',
    ]
    
    def __init__(self, SecurityIDSource=axsbe_base.SecurityIDSource_NULL, MsgType=axsbe_base.MsgType_heartbeat):
        super(axsbe_status, self).__init__(MsgType, SecurityIDSource)
        self.TradingPhaseInstrument = 0

    def load_dict(self, dict:dict):
        '''从字典加载字段'''
        #公共头
        self.SecurityIDSource = dict['SecurityIDSource']
        self.MsgType = dict['MsgType']
        self.SecurityID = dict['SecurityID']
        self.ChannelNo = dict['ChannelNo']
        self.ApplSeqNum = dict['ApplSeqNum']
        
        #消息体
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            pass
        elif self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            self.TradingPhaseInstrument = dict['TradingPhase']
            if self.MsgType==axsbe_base.MsgType_heartbeat:
                pass
            elif self.MsgType==axsbe_base.MsgType_status_sse_bond:
                self.TradingPhaseInstrument = dict['TradingPhase']
            else:
                raise Exception(f'Not support SSE status Type={self.MsgType}')
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')

    @property
    def TradingPhaseMarket(self):
        '''
        市场交易阶段：
        '''
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            return TPM.Unknown
        elif self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            if self.MsgType==axsbe_base.MsgType_heartbeat:
                return TPM.Unknown
            elif self.MsgType==axsbe_base.MsgType_status_sse_bond:
                if self.TradingPhaseInstrument==0:
                    return TPM.Starting
                if self.TradingPhaseInstrument==1:
                    return TPM.OpenCall
                elif self.TradingPhaseInstrument==2:
                    return TPM.ContinuousAutomaticMatching
                elif self.TradingPhaseInstrument==6:
                    return TPM.HangingUp
                elif self.TradingPhaseInstrument==5:
                    return TPM.Closing
                elif self.TradingPhaseInstrument==12:
                    return TPM.Ending
                elif self.TradingPhaseInstrument==11:
                    return TPM.OffMarket
                else:
                    raise Exception(f'Unknown SSE status TP={self.TradingPhaseInstrument}')
            else:
                raise Exception(f'Not support SSE status Type={self.MsgType}')
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')

    def __str__(self):
        '''打印log，只有合法的SecurityIDSource才能被打印'''
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            return f'心跳, Seq={self.ApplSeqNum}'
        elif  self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            if self.MsgType==axsbe_base.MsgType_heartbeat:
                return f'心跳, Seq={self.ApplSeqNum}'
            elif self.MsgType==axsbe_base.MsgType_status_sse_bond:
                return f'{"%06d"%self.SecurityID} TP={self.TradingPhase_str}'
            else:
                raise Exception(f'Not support SSE status Type={self.MsgType}')
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')

    @property
    def bytes_stream(self):
        '''将字段打包成字节流，重载'''
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            bin = struct.pack("<BBH9sHQB", self.SecurityIDSource, 
                                           self.MsgType,
                                           24,
                                           ("%06u  "%self.SecurityID).encode('UTF-8'),
                                           self.ChannelNo,
                                           self.ApplSeqNum,
                                           0)
        elif  self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            if self.MsgType==axsbe_base.MsgType_heartbeat:
                bin = struct.pack("<BBH9sHQB", self.SecurityIDSource, 
                                                self.MsgType,
                                                24,
                                                ("%06u  "%self.SecurityID).encode('UTF-8'),
                                                self.ChannelNo,
                                                self.ApplSeqNum,
                                                0)
            elif self.MsgType==axsbe_base.MsgType_status_sse_bond:
                bin = struct.pack("<BBH9sHQB", self.SecurityIDSource, 
                                                self.MsgType,
                                                24,
                                                ("%06u  "%self.SecurityID).encode('UTF-8'),
                                                self.ChannelNo,
                                                self.ApplSeqNum,
                                                self.TradingPhaseInstrument)
            else:
                raise Exception(f'Not support SSE status Type={self.MsgType}')
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')
        return bin

    def unpack_stream(self, bytes_i:bytes):
        '''将消息字节流解包成字段值，重载'''
        #公共头
        self.SecurityIDSource, self.MsgType, _, self.SecurityID, self.ChannelNo, self.ApplSeqNum, self.TradingPhaseInstrument = struct.unpack("<BBH9sHQB", bytes_i[:24])
        self.SecurityID = int(self.SecurityID[:6])

        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            pass
        elif self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            if self.MsgType==axsbe_base.MsgType_heartbeat:
                pass
            elif self.MsgType==axsbe_base.MsgType_status_sse_bond:
                pass
            else:
                raise Exception(f'Not support SSE status Type={self.MsgType}')
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')
        
    @property
    def ccode(self):
        '''打印与hls c相同格式的日志，重载'''
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            s = f'''
    heartbeat.Header.SecurityIDSource = __SecurityIDSource_SSZ_;
    heartbeat.Header.MsgType = __MsgType_HEARTBEAT__;
    heartbeat.Header.MsgLen = BITSIZE_SBE_SSZ_header_t_packed / 8;
    setSecurityID(heartbeat.Header.SecurityID, "{"%06d"%self.SecurityID}");
    heartbeat.Header.ChannelNo = {self.ChannelNo};
    heartbeat.Header.ApplSeqNum = {self.ApplSeqNum};
    heartbeat.Header.TradingPhase.Code0 = 0;
    heartbeat.Header.TradingPhase.Code1 = 0;
        '''
        elif  self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            if self.MsgType==axsbe_base.MsgType_heartbeat:
                s = f'''
    heartbeat.Header.SecurityIDSource = __SecurityIDSource_SSH_;
    heartbeat.Header.MsgType = __MsgType_HEARTBEAT__;
    heartbeat.Header.MsgLen = BITSIZE_SBE_SSH_header_t_packed / 8;
    setSecurityID(heartbeat.Header.SecurityID, "{"%06d"%self.SecurityID}");
    heartbeat.Header.ChannelNo = {self.ChannelNo};
    heartbeat.Header.ApplSeqNum = {self.ApplSeqNum};
    heartbeat.Header.TradingPhase = 0;
        '''
            elif self.MsgType==axsbe_base.MsgType_status_sse_bond:
                s = f'''
    status.Header.SecurityIDSource = __SecurityIDSource_SSH_;
    status.Header.MsgType = __MsgType_SSH_BOND_STATUS__;
    status.Header.MsgLen = BITSIZE_SBE_SSH_header_t_packed / 8;
    setSecurityID(status.Header.SecurityID, "{"%06d"%self.SecurityID}");
    status.Header.ChannelNo = {self.ChannelNo};
    status.Header.ApplSeqNum = {self.ApplSeqNum};
    status.Header.TickBSFlag = {self.TradingPhaseInstrument};
        '''
            else:
                raise Exception(f'Not support SSE status Type={self.MsgType}')
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')
        return s
        

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