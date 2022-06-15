import axsbe_base
import struct


class axsbe_order(axsbe_base.axsbe_base):
    
    __slots__ = [
        'SecurityIDSource',
        'MsgType',
        'SecurityID',
        'ChannelNo',
        'ApplSeqNum',
        'TransactTime',

        'Price',
        'OrderQty',
        'Side',
        'OrdType',
    ]
    
    def __init__(self, SecurityIDSource=axsbe_base.SecurityIDSource_NULL):
        super(axsbe_order, self).__init__(axsbe_base.MsgType_order, SecurityIDSource)
        self.Price = 0
        self.OrderQty = 0
        self.Side = 0
        self.OrdType = 0

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
        else:
            '''TODO:SSE'''


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
        else:
            '''TODO:SSE'''

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
        else:
            '''TODO:SSE'''

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
        else:
            '''TODO:SSE'''

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
        else:
            '''TODO:SSE'''


    def __str__(self):
        '''打印log，只有合法的SecurityIDSource才能被打印'''
        return f'{"%06d"%self.SecurityID} T={self.Type_str + self.Side_str}, Px={self.Price}, Qty={self.OrderQty}, Seq={self.ApplSeqNum}, @{self.TransactTime}'
        # return str((self.ApplSeqNum, self.Price, self.OrderQty, self.Side, self.OrdType, self.TransactTime))

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
        else:
            '''TODO:SSE'''
        return bin

    def unpack_stream_body(self, bytes_body:bytes):
        '''将消息体字节流解包成字段值，重载'''
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            self.Price,\
            self.OrderQty,\
            self.Side,\
            self.OrdType,\
            self.TransactTime, _, _ = struct.unpack("<iqBBQ2B", bytes_body)
        else:
            '''TODO:SSE'''
        
    @property
    def ccode(self):
        '''打印与hls c相同格式的日志，重载'''
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            s = f'''
    order.SecurityIDSource = 102;
    order.MsgType = __MsgType_ORDER__;
    order.MsgLen = ORDER_BYTEs;
    order.SecurityID = securityID("{"%06d"%self.SecurityID}");
    order.ChannelNo = {self.ChannelNo};
    order.ApplSeqNum = {self.ApplSeqNum};
    order.TradingPhase = {'O' if self.TradingPhaseStr == '开盘集合竞价' else 'T'};
    order.Price = {self.Price};
    order.OrderQty = {self.OrderQty};
    order.Side = {self.Side};
    order.OrdType = {self.OrdType};
    order.TransactTime = {self.TransactTime};
    order.Resv2 = 0;
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