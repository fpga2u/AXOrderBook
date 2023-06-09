# -*- coding: utf-8 -*-

import tool.axsbe_base as axsbe_base
from tool.axsbe_exe import axsbe_exe
from tool.axsbe_order import axsbe_order
from tool.axsbe_base import INSTRUMENT_TYPE, SecurityIDSource_SSE, SecurityIDSource_SZSE, SecurityIDSource_NULL
from tool.axsbe_snap_stock import axsbe_snap_stock, price_level
from enum import Enum
import pandas as pd
import numpy
from decimal import Decimal
import os

#### 交易所 板块子类型
class MARKET_SUBTYPE(Enum):
    SZSE_STK_MB  =  0   #深交所 主板   000-001
    SZSE_STK_SME =  1   #深交所 中小板 002-004
    SZSE_STK_GEM =  2   #深交所 创业板 300-309
    SZSE_STK_B   =  3   #深交所 B股    200-209
    SZSE_KZZ     =  4   #深交所 可转债
    SZSE_OTHERS  =  5   #深交所 其它

    SSE          =  5    # 上交所

def market_subtype(SecurityIDSource, SecurityID):
    if SecurityIDSource==SecurityIDSource_SZSE:
        if SecurityID<=1999:
            mst = MARKET_SUBTYPE.SZSE_STK_MB
        elif SecurityID<4999:      #中小板
            mst = MARKET_SUBTYPE.SZSE_STK_SME
        elif SecurityID>=300000 and SecurityID<309999:    #创业板 ## 创业板价格笼子 http://docs.static.szse.cn/www/disclosure/notice/general/W020200612831351578076.pdf
            mst = MARKET_SUBTYPE.SZSE_STK_GEM
        elif SecurityID>=200000 and SecurityID<209999:    #创业板 ## 创业板价格笼子 http://docs.static.szse.cn/www/disclosure/notice/general/W020200612831351578076.pdf
            mst = MARKET_SUBTYPE.SZSE_STK_B
        elif SecurityID>=120000 and SecurityID<129999:    #可转债
            mst = MARKET_SUBTYPE.SZSE_KZZ
        else:
            mst = MARKET_SUBTYPE.SZSE_OTHERS
    elif SecurityIDSource==SecurityIDSource_SSE:
            mst = MARKET_SUBTYPE.SSE

    return mst


# 板块子类型将影响快照重建中需要的 涨跌停价，临停价，有效订单价，并按照以下类型划分
#  新股首日
#  创业板首日之后
#  退市整理期首日
#  普通标的


#### 原始数据精度 ####
PRICE_SZSE_INCR_PRECISION = 10000 # 股票价格在逐笔消息中的精度：深圳4位小数
PRICE_SZSE_SNAP_PRECISION = 10000 # 股票价格在快照消息中的精度：深圳4位小数
PRICE_SZSE_SNAP_PRECLOSE_PRECISION = 10000
QTY_SZSE_PRECISION   = 100   # 数量精度：深圳2位小数
TOTALVALUETRADE_SZSE_PRECISION = 10000 # 深圳4位

PRICE_SSE_PRECISION = 1000  # 股票价格精度：上海3位小数（逐笔消息和快照消息相同）
QTY_SSE_PRECISION   = 1000  # 数量精度：上海3位小数（逐笔消息和快照消息相同）
TOTALVALUETRADE_SSE_PRECISION = 100000 # 上海5位


ORDER_PRICE_OVERFLOW = 0x7fffffff   #委托价格越界，将被钳位到32位有符号数的最大值【越界表示价格超过(2147483647 / 10^小数位数)】

## 创业板价格笼子范围
#有效竞价范围的计算结果按照四舍五入原则取至价格最小变动单位。 
#有效竞价范围上限或下限与基准价格之差的绝对值低于价格最小变动单位的，以基准价格增减一个价格最小变动单位为有效竞价范围。
CYB_cage_upper = lambda x: x+1 if x<=24 else (x*102 + 50) // 100   #创业板价格笼子上限计算，大于时被隐藏
CYB_cage_lower = lambda x: x-1 if x<=25 else (x*98 + 50) // 100    #创业板价格笼子下限计算，小于时被隐藏

## 创业板有效竞价范围
CYB_match_upper = lambda x: (x*110 + 50) // 100
CYB_match_lower = lambda x: (x*90 + 50) // 100

isTPMfreeze = lambda x:x.TradingPhaseMarket==axsbe_base.TPM.Starting\
                     or x.TradingPhaseMarket==axsbe_base.TPM.PreTradingBreaking\
                     or x.TradingPhaseMarket==axsbe_base.TPM.Breaking\
                     or x.TradingPhaseMarket>=axsbe_base.TPM.Ending

def bitSizeOf(i:int):
    n = 0
    while i:
        i>>=1
        n+=1
    return n

def str_to_dict(s:str):
    if s[:2] != "//":
        return None
    s = s[2:].split()
    s = [x.split("=") for x in s if x[-1]!='=']
    md = dict((x[0], int(x[1])) for x in s)
    return md


def dict_to_axsbe(s:dict):
    if s['MsgType'] in axsbe_base.MsgTypes_order:   #order
        order = axsbe_order(MsgType=s['MsgType'])
        order.load_dict(s)
        return order
    elif s['MsgType']==axsbe_base.MsgType_exe:   #execute
        execute = axsbe_exe()
        execute.load_dict(s)
        return execute
    elif s['MsgType'] in axsbe_base.MsgTypes_snap:   #snap
        snap = axsbe_snap_stock(MsgType=s['MsgType'])
        snap.load_dict(s)
        return snap
    else:
        return None


def axsbe_file(fileName, skip_nb=0):
    with open(fileName, 'r') as f:
        nb = 0
        while True:
            l = f.readline()
            if not l:
                break
            if l[:2] == '//':
                nb += 1
                if nb<=skip_nb:
                    continue
                msg = dict_to_axsbe(str_to_dict(l.lstrip()))
                if msg is not None:
                    yield msg
                else:
                    pass
                    # 11, 12

def extract_security(src_file, dst_file, security_list:list):
    dst_dir, _ = os.path.split(os.path.abspath(dst_file))
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    with open(src_file, 'r') as s, open(dst_file, 'w') as d:
        while True:
            l = s.readline()
            if not l:
                break
            if l[:2] == '//':
                msg = str_to_dict(l.lstrip())
                if msg['SecurityID'] in security_list:
                    d.write(l)





## 类csv格式 ##
SEC_SHFT   = 1000
MINU_SHFT  = SEC_SHFT   * 100
HOUR_SHFT  = MINU_SHFT  * 100
DAY_SHFT   = HOUR_SHFT  * 100
MONTH_SHFT = DAY_SHFT   * 100
YEAR_SHFT  = MONTH_SHFT * 100

def formatCSV2AX(df):
    '''
    SecurityIDSource
    SecurityID
    ChannelNo

    Price
    TransactTime
    '''
    df['SecurityIDSource'] = SecurityIDSource_NULL
    if not df.empty:
        if df['SecurityID'][0][-3:]=='.SZ':
            df['SecurityIDSource'] = SecurityIDSource_SZSE
        elif df['SecurityID'][0][-3:]=='.SH':
            df['SecurityIDSource'] = SecurityIDSource_SSE
            raise '上海格式尚未完成'
    df['SecurityID'] = df['SecurityID'].map(lambda x:int(x[:-3]))

    df['ChannelNo'] = 2000

    df['Price'] = df.Price.map(lambda x:int(Decimal(x)*Decimal(10000)))
    df['Qty'] = df['Qty']*100
    df["datetime"]= pd.to_datetime(df[ "datetime"])
    df['TransactTime'] = df['datetime'].map(lambda x: x.year*YEAR_SHFT + x.month*MONTH_SHFT + x.day*DAY_SHFT + x.hour*HOUR_SHFT + x.minute*MINU_SHFT + x.second*SEC_SHFT + (x.microsecond//1000))

    return df

def load_wt(fileName): #order
    '''
    csv典型值：
    #code tradetime orderqty tradeindex orderprice orderside
    "123153.SZ","2023-03-15 09:15:00.040",1000,26,119.1,"2"
    "123153.SZ","2023-03-15 09:15:00.040",1000,27,119.7,"2"
    ChannelNo 固定0
    Price 需要扩大 1e4
    OrderQty 需要扩大 100
    OrdType 固定成限价('2')
    TransactTime 由datetime转成 YYYYMMDDHHMMSSsss
    '''
    df = pd.read_csv(fileName, header=None, index_col=None, dtype={4:object}) #价格按str读入
    df.columns = ['SecurityID', 'datetime', 'Qty', 'ApplSeqNum', 'Price', 'Side']

    df['MsgType'] = axsbe_base.MsgType_order_stock

    df = formatCSV2AX(df)
    df.rename(columns={'Qty':'OrderQty'}, inplace=True)

    df['OrdType'] = ord('2')
    df['Side'] = df['Side'].map(lambda x:ord(str(x)))
    return df

def load_cj(fileName): #execute
    '''
    csv典型值：
    #code tradetime tradebsflag tradeindex tradeprice buyno tradeqty sellno tradeamount
    "123153.SZ","2023-03-15 09:15:38.870","4",15828,0,15825,10,0,0
    "123153.SZ","2023-03-15 09:15:38.950","4",15834,0,15831,10,0,0
    ChannelNo 固定0
    Price 需要扩大 1e4
    OrderQty 需要扩大 100
    OrdType 固定成限价('2')
    TransactTime 由datetime转成 YYYYMMDDHHMMSSsss
    '''
    df = pd.read_csv(fileName, header=None, index_col=None, dtype={4:object}) #价格按str读入
    df.columns = ['SecurityID', 'datetime', 'ExecType', 'ApplSeqNum', 'Price', 'BidApplSeqNum', 'Qty', 'OfferApplSeqNum', 'tradeamount']

    df['MsgType'] = axsbe_base.MsgType_exe

    df = formatCSV2AX(df)
    df.rename(columns={'Price':'LastPx', 'Qty':'LastQty'}, inplace=True)

    df['ExecType'] = df['ExecType'].map(lambda x:ord(str(x)))
    return df

def axsbe_file_csv(wtName, cjName, snapName):
    snaps = axsbe_file(snapName)
    for snap in snaps:
        if snap.HHMMSSms<91000000: #需要构造一个快照，用于重建前获取昨收、涨跌停价格
            yield snap
        else:
            break

    wt = load_wt(wtName)
    cj = load_cj(cjName)
    inc = pd.concat([wt, cj])
    for k in ['OrderQty', 'ApplSeqNum', 'Price', 'LastPx', 'BidApplSeqNum', 'LastQty', 'OfferApplSeqNum']:
        inc[k] = pd.to_numeric(inc[k].fillna(0), errors='coerce').astype('int64')


    inc.sort_values(by=['ApplSeqNum'], ascending = [True], inplace=True)

    for i in range(inc.shape[0]):
        s = inc.iloc[i].to_dict()

        for k,v in s.items():
            # print(k, type(v))
            if isinstance(v, numpy.generic):
                s[k] = numpy.asscalar(v)
            # print(k, type(v))

        msg = dict_to_axsbe(s)

        if msg is not None:
            yield msg
        else:
            pass
            # 11, 12


    snaps = axsbe_file(snapName)
    for snap in snaps:
        if snap.HHMMSSms>150100000: #需要构造一个快照，用于激活收盘后快照生成，这个快照的用于校验时一定会失败。
            yield snap
            break