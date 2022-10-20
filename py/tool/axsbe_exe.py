# -*- coding: utf-8 -*-

import tool.axsbe_base as axsbe_base
import  struct

class axsbe_exe(axsbe_base.axsbe_base):
    '''
    深交所:成交或撤单
    上交所:成交
    '''
    __slots__ = [
        'SecurityIDSource',
        'MsgType',
        'SecurityID',
        'ChannelNo',
        'ApplSeqNum',
        'TransactTime',

        'BidApplSeqNum',
        'OfferApplSeqNum',
        'LastPx',
        'LastQty',
        'ExecType',
    ]
    
    def __init__(self, SecurityIDSource=axsbe_base.SecurityIDSource_NULL):
        super(axsbe_exe, self).__init__(axsbe_base.MsgType_exe, SecurityIDSource)
        self.BidApplSeqNum = 0xffffffffffffffff
        self.OfferApplSeqNum = 0xffffffffffffffff
        self.LastPx = 0
        self.LastQty = 0
        self.ExecType = 0
        self.TransactTime = 0


    def load_dict(self, dict:dict):
        '''从字典加载字段'''
        #公共头
        self.SecurityIDSource = dict['SecurityIDSource']
        self.SecurityID = dict['SecurityID']
        self.ChannelNo = dict['ChannelNo']
        self.ApplSeqNum = dict['ApplSeqNum']

        #消息体
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            self.BidApplSeqNum = dict['BidApplSeqNum']
            self.OfferApplSeqNum = dict['OfferApplSeqNum']
            self.LastPx = dict['LastPx']
            self.LastQty = dict['LastQty']
            self.ExecType = dict['ExecType']
            self.TransactTime = dict['TransactTime']
        else:
            '''TODO:SSE'''

    def is_same(self, another):
        '''用于比较模拟撮合和历史数据是否一致'''
        SecurityID_isSame = self.SecurityID == another.SecurityID

        BidApplSeqNum_isSame = self.BidApplSeqNum == another.BidApplSeqNum
        OfferApplSeqNum_isSame = self.OfferApplSeqNum == another.OfferApplSeqNum

        LastPx_isSame = self.LastPx == another.LastPx
        LastQty_isSame = self.LastQty == another.LastQty
        ExecType_isSame = self.ExecType == another.ExecType

        if SecurityID_isSame \
            and BidApplSeqNum_isSame \
            and OfferApplSeqNum_isSame \
            and LastPx_isSame \
            and LastQty_isSame \
            and ExecType_isSame :
            return True
        else:
            return False

    @property
    def ExecType_str(self):
        '''打印执行类型'''
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            if self.ExecType==ord('F'):
                return '成交'
            elif self.ExecType==ord('4'):
                return '撤单'
            raise RuntimeError(f"非法执行类型:{self.ExecType}")
        else:
            '''TODO:SSE'''

    def __str__(self):
        '''打印log，只有合法的SecurityIDSource才能被打印'''
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            return f'{"%06d"%self.SecurityID} T={self.ExecType_str}, Px={self.LastPx}, Qty={self.LastQty}, Seq={self.ApplSeqNum}, BidSeq={self.BidApplSeqNum}, AskSeq={self.OfferApplSeqNum}, @{self.TransactTime}'
        else:
            '''TODO:SSE'''

    @property
    def bytes_stream(self):
        '''将字段打包成字节流，重载'''
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            #SecurityIDSource=102
            bin = struct.pack("<B", axsbe_base.SecurityIDSource_SZSE)
            #MsgType=191
            bin += struct.pack("<B", axsbe_base.MsgType_exe)
            #MsgLen=64
            bin += struct.pack("<H", 64)
            #SecurityID=000997
            bin += struct.pack("<9s", ("%06u  "%self.SecurityID).encode('UTF-8'))
            #ChannelNo=2013
            bin += struct.pack("<H", self.ChannelNo)
            #ApplSeqNum=398788
            bin += struct.pack("<Q", self.ApplSeqNum)
            #TradingPhase=0
            bin += struct.pack("<B", 0xff)
            #BidApplSeqNum=242000
            bin += struct.pack("<Q", self.BidApplSeqNum)
            #OfferApplSeqNum=0
            bin += struct.pack("<Q", self.OfferApplSeqNum)
            #LastPx=0
            bin += struct.pack("<i", self.LastPx)
            #LastQty=10000
            bin += struct.pack("<q", self.LastQty)
            #ExecType=52
            bin += struct.pack("<B", self.ExecType)
            #TransactTime=20190311093000140
            bin += struct.pack("<Q", self.TransactTime)
            #resv=
            bin += struct.pack("<3B", 0, 0, 0)
        else:
            '''TODO:SSE'''
        return bin

    def unpack_stream(self, bytes_i:bytes):
        '''将消息字节流解包成字段值，重载'''
        #公共头
        self.SecurityIDSource, _, _, self.SecurityID, self.ChannelNo, self.ApplSeqNum = struct.unpack("<BBH9sHQ", bytes_i[:23])
        self.SecurityID = int(self.SecurityID[:6])

        #消息体
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            self.BidApplSeqNum, \
            self.OfferApplSeqNum, \
            self.LastPx, \
            self.LastQty, \
            self.ExecType, \
            self.TransactTime, _, _, _, = struct.unpack("<QQiqBQ3B", bytes_i[24:])
        else:
            '''TODO:SSE'''


    @property
    def ccode(self):
        '''打印与hls c相同格式的日志，重载'''
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            s = f'''
    exec.SecurityIDSource = 102;
    exec.MsgType = __MsgType_SSZ_EXECUTION__;
    exec.MsgLen = EXEC_BYTEs;
    exec.SecurityID = securityID("{"%06d"%self.SecurityID}");
    exec.ChannelNo = {self.ChannelNo};
    exec.ApplSeqNum = {self.ApplSeqNum};
    exec.TradingPhase = 255;
    exec.BidApplSeqNum = {self.BidApplSeqNum};
    exec.OfferApplSeqNum = {self.OfferApplSeqNum};
    exec.LastPx = {self.LastPx};
    exec.LastQty = {self.LastQty};
    exec.ExecType = '4{self.ExecType};
    exec.TransactTime = {self.TransactTime};
    exec.Resv3 = 0;
    '''
        else:
            '''TODO:SSE'''

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
