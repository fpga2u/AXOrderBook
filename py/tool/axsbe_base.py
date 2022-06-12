import abc
import numpy as np

## 交易所代码
SecurityIDSource_SSE = 101
SecurityIDSource_SZSE = 102

## 消息类型
MsgType_exe   = 191
MsgType_order = 192
MsgType_snap  = 111


## TradingPhase 交易阶段代码 Code0
TP_Starting = 'S'  #启动（开市前）
TP_OpenCall = 'O'  #开盘集合竞价
TP_preTradingBreaking = 'p'    #集合竞价与连续竞价之间
TP_Trading = 'T'   #连续竞价上半场
TP_Breaking = 'B'  #休市
TP_CloseCall = 'C' #收盘集合竞价
TP_Ending = 'E'    #已闭市
TP_HangingUp = 'H' #临时停牌
TP_AfterTrading = 'A'  #盘后交易
TP_VolatilityBreaking = 'V'    #波动性中断
TradingPhaseMarket_str = {
    TP_Starting : '启动',
    TP_OpenCall : '开盘集合竞价',
    TP_preTradingBreaking : '集合竞价与连续竞价之间',
    TP_Trading : '连续竞价',
    TP_Breaking : '休市',
    TP_CloseCall : '收盘集合竞价',
    TP_Ending : '已闭市',
    TP_HangingUp : '临时停牌',
    TP_AfterTrading : '盘后交易',
    TP_VolatilityBreaking : '波动性中断',
    None : '无意义',
}

## TradingPhase 交易阶段代码 Code1
TP_Normal = 0
TP_NoTrade = 1
TradingPhaseSecurity_str = {
    TP_Normal : '正常',
    TP_NoTrade : '全天停牌',
    None : '无意义',
}


class axsbe_base(abc.ABC):
    '''
    sbe消息基类：
    目前先按照深交所精度来实现，待需要加入上交所支持时通过SecurityIDSource实现精度切换。
    '''
    def __init__(self, MsgType, SecurityIDSource):
        self.SecurityIDSource = SecurityIDSource #"证券代码源101=上交所;102=深交所;103=香港交易所"
        self.MsgType = MsgType
        self.SecurityID = -1
        self.ChannelNo = 0xffff
        self.ApplSeqNum = 0xffffffffffffffff
        self.TransactTime = 0

        self._tick = None
        self._HHMMSSms = None
        self._ms = None

    @property
    def ms(self):
        '''日内时间戳，精度ms，可用于计算'''
        if self._ms is None:
            self.tick
        return self._ms

    @property
    def HHMMSSms(self):
        '''日内时间戳，可比较'''
        if self._HHMMSSms is None:
            if self.SecurityIDSource == SecurityIDSource_SZSE:
                self._HHMMSSms = self.TransactTime % 1000000000
            else:
                '''TODO:SSE'''
        return self._HHMMSSms

    @property
    def tick(self):
        '''日内时间戳，可阅读'''
        if self._tick is None:
            t = self.HHMMSSms
            ms = t % 1000
            ss = int((t % (100000))   / 1000)
            mm = int((t % (10000000)) / 100000)
            hh = int((t )             / 10000000)
            self._tick = f"{hh}:{mm}:{ss}.{ms}"
            self._ms = ms + ss * 1000 + mm * 60 * 1000 + hh * 3600 * 1000
        return self._tick
        
    def is_opened(self):
        '''已过开盘集合竞价'''
        if self.HHMMSSms < 92500000:
            return False
        else:
            return True

            
    @property
    def TradingPhaseMarket(self):
        '''
        市场交易阶段：
        对于快照行情，其内部历史数据自带市场交易阶段字段，将重载本接口。
        对于逐笔委托和逐笔成交，利用时戳判断交易阶段。
        '''
        t = self.HHMMSSms
        if t < 91500000:
            return TP_Starting
        elif t < 92500000:
            return TP_OpenCall
        elif t < 93000000:
            return TP_preTradingBreaking
        elif t < 113000000:
            return TP_Trading
        elif t < 130000000:
            return TP_Breaking
        elif t < 145700000:
            return TP_Trading
        elif t < 150000000:
            return TP_CloseCall
        else:
            return TP_Ending

    @property
    def TradingPhase_str(self):
        return TradingPhaseMarket_str(self.TradingPhaseMarket)

    @property
    @abc.abstractmethod
    def bytes_stream(self)->bytes(): 
        '''将字段打包成字节流，派生类需重载'''
        return bytes()
        
    @property
    def bytes_str(self):
        '''打印字节流'''
        bin = self.bytes_stream
        l = ["%02X"%i for i in bin]
        return " ".join(l)

    @property
    def bytes_np(self):
        '''将字段打包成numpy字节流'''
        bin = self.bytes_stream
        np_array = np.frombuffer(bin, dtype=np.uint8)
        # print(np_array.shape)
        # print(np_array)
        return np_array

    @abc.abstractmethod
    def unpack_stream(self, bytes_i:bytes):
        '''将字节流解包成字段值，派生类需重载'''
        return NotImplemented

    def unpack_np(self, np_i:np.ndarray):
        '''将numpy字节流解包成字段值'''
        bytes_i = np_i.tobytes()
        self.unpack_stream(bytes_i)
        
    @property
    @abc.abstractmethod
    def ccode(self)->str:
        '''打印与hls c相同格式的日志'''
        return NotImplemented


    @abc.abstractmethod
    def save(self):
        return NotImplemented

    @abc.abstractmethod
    def load(self, data):
        return NotImplemented
