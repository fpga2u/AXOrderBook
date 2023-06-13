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
        'TransactTime',     # SH-STOCK.TradeTime;   SH-BOND.TickTime

        'BidApplSeqNum',    # SH-STOCK.TradeBuyNo;  SH-BOND.BuyOrderNo
        'OfferApplSeqNum',  # SH-STOCK.TradeSellNo; SH-BOND.SellOrderNo
        'LastPx',           # SH-STOCK.LastPx;      SH-BOND.Price
        'LastQty',          # SH-STOCK.LastQty;     SH-BOND.Qty
        'ExecType',         # SH-STOCK.TradeBSFlag

        'BizIndex',         #SH-STOCK

        'TradeMoney',       #SH-BOND
    ]
    
    def __init__(self, SecurityIDSource=axsbe_base.SecurityIDSource_NULL, MsgType=axsbe_base.MsgType_exe_stock):
        super(axsbe_exe, self).__init__(MsgType, SecurityIDSource)
        self.BidApplSeqNum = 0xffffffffffffffff
        self.OfferApplSeqNum = 0xffffffffffffffff
        self.LastPx = 0
        self.LastQty = 0
        self.ExecType = 0
        self.TransactTime = 0

        self.BizIndex = 0 #仅上海有效，有效时从1开始

        self.TradeMoney = 0

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

        elif self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            if self.MsgType==axsbe_base.MsgType_exe_stock:
                self.BidApplSeqNum = dict['BidApplSeqNum']
                self.OfferApplSeqNum = dict['OfferApplSeqNum']
                self.LastPx = dict['LastPx']
                self.LastQty = dict['LastQty']
                self.ExecType = dict['ExecType']
                self.TransactTime = dict['TransactTime']

                self.BizIndex = dict['BizIndex']
            elif self.MsgType==axsbe_base.MsgType_exe_sse_bond:
                self.ExecType = dict['TradingPhase']
                self.BidApplSeqNum = dict['BuyOrderNo']
                self.OfferApplSeqNum = dict['SellOrderNo']
                self.LastPx = dict['Price']
                self.LastQty = dict['Qty']
                self.TradeMoney = dict['TradeMoney']
                self.TransactTime = dict['TickTime']
            else:
                raise Exception(f'Not support SSE exec Type={self.MsgType}')
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')

    def is_same(self, another):
        '''用于比较模拟撮合和历史数据是否一致'''
        SecurityID_isSame = self.SecurityID == another.SecurityID

        BidApplSeqNum_isSame = self.BidApplSeqNum == another.BidApplSeqNum
        OfferApplSeqNum_isSame = self.OfferApplSeqNum == another.OfferApplSeqNum

        LastPx_isSame = self.LastPx == another.LastPx
        LastQty_isSame = self.LastQty == another.LastQty
        ExecType_isSame = self.ExecType == another.ExecType

        BizIndex_isSame = self.BizIndex == another.BizIndex

        TradeMoney_isSame = self.TradeMoney == another.TradeMoney
        if SecurityID_isSame \
            and BidApplSeqNum_isSame \
            and OfferApplSeqNum_isSame \
            and LastPx_isSame \
            and LastQty_isSame \
            and ExecType_isSame \
            and BizIndex_isSame \
            and TradeMoney_isSame:
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
        elif  self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE: # 内外盘标志: 'B'=外盘，主动买; 'S'=内盘，主动卖; 'N'=未知
            if self.ExecType==ord('B'):
                return '外盘'
            elif self.ExecType==ord('S'):
                return '内盘'
            elif self.ExecType==ord('N'):
                return '未知'
            raise RuntimeError(f"非法 TradeBSFlag={self.ExecType}")
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')

    def __str__(self):
        '''打印log，只有合法的SecurityIDSource才能被打印'''
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            return f'{"%06d"%self.SecurityID} T={self.ExecType_str}, Px={self.LastPx}, Qty={self.LastQty}, Seq={self.ApplSeqNum}, BidSeq={self.BidApplSeqNum}, AskSeq={self.OfferApplSeqNum}, @{self.TransactTime}'
        elif  self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            if self.MsgType==axsbe_base.MsgType_exe_stock:
                return f'{"%06d"%self.SecurityID} T={self.ExecType_str}, Px={self.LastPx}, Qty={self.LastQty}, Seq={self.ApplSeqNum}, BidSeq={self.BidApplSeqNum}, AskSeq={self.OfferApplSeqNum}, BizIndex={self.BizIndex}, @{self.TransactTime}'
            elif self.MsgType==axsbe_base.MsgType_exe_sse_bond:
                return f'{"%06d"%self.SecurityID} T={self.ExecType_str}, Px={self.LastPx}, Qty={self.LastQty}, Seq={self.ApplSeqNum}, BidSeq={self.BidApplSeqNum}, AskSeq={self.OfferApplSeqNum}, @{self.TransactTime}'
            else:
                raise Exception(f'Not support SSE exec Type={self.MsgType}')
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')

    @property
    def bytes_stream(self):
        '''将字段打包成字节流，重载'''
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            #SecurityIDSource=102
            bin = struct.pack("<B", axsbe_base.SecurityIDSource_SZSE)
            #MsgType=191
            bin += struct.pack("<B", self.MsgType)
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
        elif  self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            #SecurityIDSource=101
            bin = struct.pack("<B", axsbe_base.SecurityIDSource_SSE)
            #MsgType=191
            bin += struct.pack("<B", self.MsgType)
            if self.MsgType==axsbe_base.MsgType_exe_stock:
                #MsgLen=72
                bin += struct.pack("<H", 72)
            elif self.MsgType==axsbe_base.MsgType_exe_sse_bond:
                #MsgLen=72
                bin += struct.pack("<H", 64)
            else:
                raise Exception(f'Not support SSE exec Type={self.MsgType}')
            #SecurityID=600519
            bin += struct.pack("<9s", ("%06u  "%self.SecurityID).encode('UTF-8'))
            #ChannelNo=6
            bin += struct.pack("<H", self.ChannelNo)
            #ApplSeqNum=25741
            bin += struct.pack("<Q", self.ApplSeqNum)
            if self.MsgType==axsbe_base.MsgType_exe_stock:
                #TradingPhase=0
                bin += struct.pack("<B", 0xff)
            elif self.MsgType==axsbe_base.MsgType_exe_sse_bond:
                #TickBSFlag=0
                bin += struct.pack("<B", self.ExecType)
            #BidApplSeqNum=234313
            bin += struct.pack("<Q", self.BidApplSeqNum)
            #OfferApplSeqNum=232172
            bin += struct.pack("<Q", self.OfferApplSeqNum)
            #LastPx=1086000
            bin += struct.pack("<i", self.LastPx)
            #LastQty=1000000
            bin += struct.pack("<q", self.LastQty)

            if self.MsgType==axsbe_base.MsgType_exe_stock:
                #ExecType=66
                bin += struct.pack("<B", self.ExecType)
                #TransactTime=14302506
                bin += struct.pack("<I", self.TransactTime)
                #resv=
                bin += struct.pack("<7B", 0, 0, 0, 0, 0, 0, 0)
                #BizIndex=12000
                bin += struct.pack("<Q", self.BizIndex)
            elif self.MsgType==axsbe_base.MsgType_exe_sse_bond:
                #TradeMoney
                bin += struct.pack("<q", self.TradeMoney)
                #TransactTime=14302506
                bin += struct.pack("<I", self.TransactTime)
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')
        return bin

    def unpack_stream(self, bytes_i:bytes):
        '''将消息字节流解包成字段值，重载'''
        #公共头
        self.SecurityIDSource, self.MsgType, _, self.SecurityID, self.ChannelNo, self.ApplSeqNum, self.ExecType = struct.unpack("<BBH9sHQB", bytes_i[:24])
        self.SecurityID = int(self.SecurityID[:6])

        #消息体
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            self.BidApplSeqNum, \
            self.OfferApplSeqNum, \
            self.LastPx, \
            self.LastQty, \
            self.ExecType, \
            self.TransactTime, _, _, _, = struct.unpack("<QQiqBQ3B", bytes_i[24:])
        elif self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            if self.MsgType==axsbe_base.MsgType_exe_stock:
                self.BidApplSeqNum, \
                self.OfferApplSeqNum, \
                self.LastPx, \
                self.LastQty, \
                self.ExecType, \
                self.TransactTime, \
                _, _, _, _, _, _, _, \
                self.BizIndex = struct.unpack("<QQiqBI7BQ", bytes_i[24:])
            elif self.MsgType==axsbe_base.MsgType_exe_sse_bond:
                self.BidApplSeqNum, \
                self.OfferApplSeqNum, \
                self.LastPx, \
                self.LastQty, \
                self.TradeMoney, \
                self.TransactTime = struct.unpack("<QQiqqI", bytes_i[24:])
            else:
                raise Exception(f'Not support SSE exec Type={self.MsgType}')
        else:
            raise Exception(f'Not support SecurityIDSource={self.SecurityIDSource}')


    @property
    def ccode(self):
        '''打印与hls c相同格式的日志，重载'''
        if self.SecurityIDSource == axsbe_base.SecurityIDSource_SZSE:
            s = f'''
    exec.Header.SecurityIDSource = __SecurityIDSource_SSZ_;
    exec.Header.MsgType = __MsgType_SSZ_EXECUTION__;
    exec.Header.MsgLen = BITSIZE_SBE_SSZ_exe_t_packed / 8;
    setSecurityID(exec.Header.SecurityID, "{"%06d"%self.SecurityID}");
    exec.Header.ChannelNo = {self.ChannelNo};
    exec.Header.ApplSeqNum = {self.ApplSeqNum};
    exec.Header.TradingPhase.Code0 = 0;
    exec.Header.TradingPhase.Code1 = 0;
    exec.BidApplSeqNum = {self.BidApplSeqNum};
    exec.OfferApplSeqNum = {self.OfferApplSeqNum};
    exec.LastPx = {self.LastPx};
    exec.LastQty = {self.LastQty};
    exec.ExecType = '{self.ExecType};
    exec.TransactTime = {self.TransactTime};
    exec.Resv[0] = 0;
    exec.Resv[1] = 0;
    exec.Resv[2] = 0;
    '''
        elif self.SecurityIDSource == axsbe_base.SecurityIDSource_SSE:
            if self.MsgType==axsbe_base.MsgType_exe_stock:
                s = f'''
    exec.Header.SecurityIDSource = __SecurityIDSource_SSH_;
    exec.Header.MsgType = __MsgType_SSH_EXECUTION__;
    exec.Header.MsgLen = BITSIZE_SBE_SSH_exe_t_packed / 8;
    setSecurityID(exec.Header.SecurityID, "{"%06d"%self.SecurityID}");
    exec.Header.ChannelNo = {self.ChannelNo};
    exec.Header.ApplSeqNum = {self.ApplSeqNum};
    exec.Header.TradingPhase.Code0 = 0;
    exec.Header.TradingPhase.Code1 = 0;
    exec.TradeBuyNo = {self.BidApplSeqNum};
    exec.TradeSellNo = {self.OfferApplSeqNum};
    exec.LastPx = {self.LastPx};
    exec.LastQty = {self.LastQty};
    exec.TradeBSFlag = '{self.ExecType};
    exec.TradeTime = {self.TransactTime};
    exec.Resv[0] = 0;
    exec.Resv[1] = 0;
    exec.Resv[2] = 0;
    exec.Resv[3] = 0;
    exec.Resv[4] = 0;
    exec.Resv[5] = 0;
    exec.Resv[6] = 0;
    exec.BizIndex = {self.BizIndex};
    '''
            elif self.MsgType==axsbe_base.MsgType_exe_sse_bond:
                s = f'''
    exec.Header.SecurityIDSource = __SecurityIDSource_SSH_;
    exec.Header.MsgType = __MsgType_SSH_BOND_TRADE__;
    exec.Header.MsgLen = BITSIZE_SBE_SSH_bond_trade_t_packed / 8;
    setSecurityID(exec.Header.SecurityID, "{"%06d"%self.SecurityID}");
    exec.Header.ChannelNo = {self.ChannelNo};
    exec.Header.ApplSeqNum = {self.ApplSeqNum};
    exec.Header.TickBSFlag = {self.ExecType};
    exec.BuyOrderNo = {self.BidApplSeqNum};
    exec.SellOrderNo = {self.OfferApplSeqNum};
    exec.Price = {self.LastPx};
    exec.Qty = {self.LastQty};
    exec.TradeMoney = '{self.TradeMoney};
    exec.TickTime = {self.TransactTime};
    '''
            else:
                raise Exception(f'Not support SSE exec Type={self.MsgType}')
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
