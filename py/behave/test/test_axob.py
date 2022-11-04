# -*- coding: utf-8 -*-

from tool.axsbe_base import SecurityIDSource_SZSE, TPM, INSTRUMENT_TYPE
from tool.test_util import *
from tool.msg_util import *
from behave.axob import AXOB
import os

def TEST_axob_SL():
    '''TODO: axob save/load'''
    pass


@timeit
def TEST_axob_openCall(date, instrument:int, n_max=500, SecurityIDSource=SecurityIDSource_SZSE):
    md_file = f'data/{date}/AX_sbe_szse_{instrument:06d}.log'
    if not os.path.exists(md_file):
        raise f"{md_file} not exists"

    axob = AXOB(instrument, SecurityIDSource, INSTRUMENT_TYPE.STOCK)

    n = 0
    for msg in axsbe_file(md_file):
        if msg.TradingPhaseMarket>TPM.OpenCall:
            print(f'openCall over, n={n}')
            break
        axob.onMsg(msg)
        n += 1
        if n>=n_max:
            print(f'nb over, n={n}')
            break

    print("TEST_msg_ms done")
    return


@timeit
def TEST_axob_openCall_bat(source_file, instrument_list:list, n_max=500, SecurityIDSource=SecurityIDSource_SZSE):
    if not os.path.exists(source_file):
        raise f"{source_file} not exists"

    axobs = {}
    for x in instrument_list:
        axobs[x] = AXOB(x, SecurityIDSource, INSTRUMENT_TYPE.STOCK)

    n = 0 #只计算在 instrument_list 内的消息
    for msg in axsbe_file(source_file):
        if msg.TradingPhaseMarket>TPM.OpenCall:
            print(f'openCall over, n={n}')
            break
        x = msg.SecurityID
        if x not in axobs:
            continue

        axobs[x].onMsg(msg)
        n += 1
        if n_max>0 and n>=n_max:
            print(f'nb over, n={n}')
            break

    for x in instrument_list:
        axobs[x].are_you_ok()

    print("TEST_axob_openCall_bat done")
    return

