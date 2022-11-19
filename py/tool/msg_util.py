# -*- coding: utf-8 -*-

import tool.axsbe_base as axsbe_base
from tool.axsbe_exe import axsbe_exe
from tool.axsbe_order import axsbe_order
from tool.axsbe_base import INSTRUMENT_TYPE, SecurityIDSource_SSE, SecurityIDSource_SZSE
from tool.axsbe_snap_stock import axsbe_snap_stock, price_level
from enum import Enum

# CHNL_STOCK = 0
# CHNL_FUND = 1
# CHNL_KZZ = 2
# CHNL_QZ = 3
# CHNL_OPTION = 4

# def chnl_type(msg):
#     if msg.SecurityIDSource==axsbe_base.SecurityIDSource_SSE:
#         if isinstance(msg, axsbe_exe) or isinstance(msg, axsbe_order):
#             if msg.ChannelNo>=2010 and msg.ChannelNo<=2019:
#                 return CHNL_STOCK
#             elif msg.ChannelNo>=2020 and msg.ChannelNo<=2029:
#                 return CHNL_FUND
#             elif msg.ChannelNo>=2030 and msg.ChannelNo<=2039:
#                 return CHNL_KZZ
#             elif msg.ChannelNo>=2040 and msg.ChannelNo<=2049:
#                 return CHNL_QZ
#             elif msg.ChannelNo>=2050 and msg.ChannelNo<=2059:
#                 return CHNL_OPTION
#             else:
#                 return None
#         elif isinstance(msg, axsbe_snap_stock):
#                 return CHNL_STOCK
#         else:
#             return None

#     if msg.SecurityIDSource==axsbe_base.SecurityIDSource_SZSE:
#         '''TODO:'''
#         pass
#     return None

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

def str_to_dict(s:str):
    if s[:2] != "//":
        return None
    s = s[2:].split()
    s = [x.split("=") for x in s if x[-1]!='=']
    md = dict((x[0], int(x[1])) for x in s)
    return md


def dict_to_axsbe(s:dict):
    if s['MsgType']==axsbe_base.MsgType_order:   #order
        order = axsbe_order()
        order.load_dict(s)
        return order
    elif s['MsgType']==axsbe_base.MsgType_exe:   #execute
        execute = axsbe_exe()
        execute.load_dict(s)
        return execute
    elif s['MsgType']==axsbe_base.MsgType_snap:   #snap
        snap = axsbe_snap_stock()
        snap.load_dict(s)
        return snap
    else:
        return None


def axsbe_file(fileName, skip_nb=0):
    with open(fileName, "r") as f:
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
    with open(src_file, "r") as s, open(dst_file, 'w') as d:
        while True:
            l = s.readline()
            if not l:
                break
            if l[:2] == '//':
                msg = str_to_dict(l.lstrip())
                if msg['SecurityID'] in security_list:
                    d.write(l)

