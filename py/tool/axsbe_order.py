# -*- coding: utf-8 -*-

import tool.axsbe_base as axsbe_base
import struct


class axsbe_order(axsbe_base.axsbe_base):
    '''
    深交所:新增委托
    上交所:新增委托或撤单
    '''
    
    __slots__ = [
        'SecurityIDSource',
        'MsgType',
        'SecurityID',
        'ChannelNo',
        'ApplSeqNum',
        'TransactTime',     #SH.OrderTime

        'Price',
        'OrderQty',
        'Side',
        'OrdType',

        'OrderNo',          #SH
        'BizIndex',         #SH
    ]
    
    def __init__(self, SecurityIDSource=axsbe_base.SecurityIDSource_NULL):
        super(axsbe_order, self).__init__(axsbe_base.MsgType_order, SecurityIDSource)
        self.Price = 0
        self.OrderQty = 0
        self.Side = 0
        self.OrdType = 0

        self.OrderNo = 0
        self.BizIndex = 0

    def load_dict(self, dict:dict):
        '''从字典加载字段'''
        #公共头
        self.SecurityIDSource = dict['SecurityIDSource']
        self.SecurityID = dict['SecurityID']
        self.ChannelNo = dict['ChannelNo']
        self.ApplSeqNum = dict['ApplSeqNum']
        
        #消息体
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            self.Price = dict['Price']
            self.OrderQty = dict['OrderQty']
            self.Side = dict['Side']
            self.TransactTime = dict['TransactTime']
            self.OrdType = dict['OrdType']
        elif self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            self.OrderNo = dict['OrderNo']
            self.Price = dict['Price']
            self.OrderQty = dict['OrderQty']
            self.OrdType = dict['OrdType']
            self.Side = dict['Side']
            self.TransactTime = dict['TransactTime']
            self.BizIndex = dict['BizIndex']
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')


    @property
    def Side_str(self):
        '''打印委托方向'''
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            if self.Side==ord('1'):
                return '买入'
            elif self.Side==ord('2'):
                return '卖出'
            elif self.Side==ord('G'):   #TODO:暂无历史数据
                return '借入'
            elif self.Side==ord('F'):   #TODO:暂无历史数据
                return '出借'
            raise RuntimeError(f"非法委托方向:{self.Side}")
        elif self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            if self.Side==ord('B'):
                return '买入'
            elif self.Side==ord('S'):
                return '卖出'
            raise RuntimeError(f"非法委托方向:{self.Side}")
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')

    @property
    def Type_str(self):
        '''打印委托类型'''
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            if self.OrdType==ord('1'):
                return '市价'
            elif self.OrdType==ord('2'):
                return '限价'
            elif self.OrdType==ord('U'):
                return '本方最优'
            raise RuntimeError(f"非法委托类型:{self.OrdType}")
        elif self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            if self.OrdType==ord('A'):
                return '新增'
            elif self.OrdType==ord('D'):
                return '删除'
            raise RuntimeError(f"非法委托类型:{self.OrdType}")
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')

    def setSide(self, s):
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            if s == "买入":
                self.Side = ord('1')
            elif s == "卖出":
                self.Side = ord('2')
            elif s == "借入":
                self.Side = ord('G')
            elif s == "出借":
                self.Side = ord('F')
            else:
                raise RuntimeError(f"非法委托方向:{s}")
        elif self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            if s == "买入":
                self.Side = ord('B')
            elif s == "卖出":
                self.Side = ord('S')
            else:
                raise RuntimeError(f"非法委托方向:{s}")
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')

    def setType(self, t):
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            if t == "市价":
                self.OrdType = ord('1')
            elif t == "限价":
                self.OrdType = ord('2')
            elif t == "本方最优":
                self.OrdType = ord('U')
            else:
                raise RuntimeError(f"非法委托类型:{t}")
        elif self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            if t == "新增":
                self.Side = ord('A')
            elif t == "删除":
                self.Side = ord('D')
            else:
                raise RuntimeError(f"非法委托类型:{t}")
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')


    def __str__(self):
        '''打印log，只有合法的SecurityIDSource才能被打印'''
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            return f'{"%06d"%self.SecurityID} T={self.Type_str + self.Side_str}, Px={self.Price}, Qty={self.OrderQty}, Seq={self.ApplSeqNum}, @{self.TransactTime}'
        elif  self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            return f'{"%06d"%self.SecurityID} T={self.Type_str + self.Side_str}, Px={self.Price}, Qty={self.OrderQty}, Seq={self.ApplSeqNum}, OrderNo={self.OrderNo}, BizIndex={self.BizIndex}, @{self.TransactTime}'
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')

    @property
    def bytes_stream(self):
        '''将字段打包成字节流，重载'''
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            #SecurityIDSource=102
            bin = struct.pack("<B", axsbe_base.SecurityIDSource_SZSE)
            #MsgType=192
            bin += struct.pack("<B", axsbe_base.MsgType_order)
            #MsgLen=48
            bin += struct.pack("<H", 48)
            #SecurityID=000997
            bin += struct.pack("<9s", ("%06u  "%self.SecurityID).encode('UTF-8'))
            #ChannelNo=2013
            bin += struct.pack("<H", self.ChannelNo)
            #ApplSeqNum=399751
            bin += struct.pack("<Q", self.ApplSeqNum)
            #TradingPhase=0
            bin += struct.pack("<B", 0)
            #Price=182100
            bin += struct.pack("<i", self.Price)
            #OrderQty=100000
            bin += struct.pack("<q", self.OrderQty)
            #Side=49
            bin += struct.pack("<B", self.Side)
            #OrdType=50
            bin += struct.pack("<B", self.OrdType)
            #TransactTime=20190311093000150
            bin += struct.pack("<Q", self.TransactTime)
            #resv=
            bin += struct.pack("<2B", 0, 0)
        elif  self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            #SecurityIDSource=101
            bin = struct.pack("<B", axsbe_base.SecurityIDSource_SSE)
            #MsgType=192
            bin += struct.pack("<B", axsbe_base.MsgType_order)
            #MsgLen=64
            bin += struct.pack("<H", 64)
            #SecurityID=600519
            bin += struct.pack("<9s", ("%06u  "%self.SecurityID).encode('UTF-8'))
            #ChannelNo=6
            bin += struct.pack("<H", self.ChannelNo)
            #ApplSeqNum=229692
            bin += struct.pack("<Q", self.ApplSeqNum)
            #TradingPhase=0
            bin += struct.pack("<B", 0)
            #OrderNo=225666
            bin += struct.pack("<q", self.OrderNo)
            #Price=1808080
            bin += struct.pack("<i", self.Price)
            #OrderQty=100000
            bin += struct.pack("<q", self.OrderQty)
            #OrdType=65
            bin += struct.pack("<B", self.OrdType)
            #Side=83
            bin += struct.pack("<B", self.Side)
            #TransactTime=9300128
            bin += struct.pack("<I", self.TransactTime)
            #resv=
            bin += struct.pack("<6B", 0, 0, 0, 0, 0, 0)
            #BizIndex=252932
            bin += struct.pack("<Q", self.BizIndex)
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')
        return bin

    def unpack_stream(self, bytes_i:bytes):
        '''将消息字节流解包成字段值，重载'''
        #公共头
        self.SecurityIDSource, _, _, self.SecurityID, self.ChannelNo, self.ApplSeqNum = struct.unpack("<BBH9sHQ", bytes_i[:23])
        self.SecurityID = int(self.SecurityID[:6])

        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            self.Price,\
            self.OrderQty,\
            self.Side,\
            self.OrdType,\
            self.TransactTime, _, _ = struct.unpack("<iqBBQ2B", bytes_i[24:])
        elif  self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            self.OrderNo,\
            self.Price,\
            self.OrderQty,\
            self.OrdType,\
            self.Side,\
            self.TransactTime, \
            _, _, _, _, _, _, \
            self.BizIndex = struct.unpack("<qiqBBI6BQ", bytes_i[24:])
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')
        
    @property
    def ccode(self):
        '''打印与hls c相同格式的日志，重载'''
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            s = f'''
    order.Header.SecurityIDSource = __SecurityIDSource_SSZ_;
    order.Header.MsgType = __MsgType_SSZ_ORDER__;
    order.Header.MsgLen = BITSIZE_SBE_SSZ_ord_t_packed / 8;
    setSecurityID(order.Header.SecurityID, "{"%06d"%self.SecurityID}");
    order.Header.ChannelNo = {self.ChannelNo};
    order.Header.ApplSeqNum = {self.ApplSeqNum};
    order.Header.TradingPhase.Code0 = 0;
    order.Header.TradingPhase.Code1 = 0;
    order.Price = {self.Price};
    order.OrderQty = {self.OrderQty};
    order.Side = {self.Side};
    order.OrdType = {self.OrdType};
    order.TransactTime = {self.TransactTime};
    order.Resv[0] = 0;
    order.Resv[1] = 0;
        '''
    # order.TradingPhase = {'O' if self.TradingPhaseStr == '开盘集合竞价' else 'T'};
        elif  self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            s = f'''
    order.Header.SecurityIDSource = __SecurityIDSource_SSH_;
    order.Header.MsgType = __MsgType_SSH_ORDER__;
    order.Header.MsgLen = BITSIZE_SBE_SSH_ord_t_packed / 8;
    setSecurityID(order.Header.SecurityID, "{"%06d"%self.SecurityID}");
    order.Header.ChannelNo = {self.ChannelNo};
    order.Header.ApplSeqNum = {self.ApplSeqNum};
    order.Header.TradingPhase.Code0 = 0;
    order.Header.TradingPhase.Code1 = 0;
    order.OrderNo = {self.OrderNo};
    order.Price = {self.Price};
    order.OrderQty = {self.OrderQty};
    order.OrdType = {self.OrdType};
    order.Side = {self.Side};
    order.OrderTime = {self.TransactTime};
    order.Resv[0] = 0;
    order.Resv[1] = 0;
    order.Resv[2] = 0;
    order.Resv[3] = 0;
    order.Resv[4] = 0;
    order.Resv[5] = 0;
    order.BizIndex = {self.BizIndex};
        '''
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