# -*- coding: utf-8 -*-

from tool.axsbe_base import SecurityIDSource_SZSE, TPM, INSTRUMENT_TYPE
from tool.test_util import *
from tool.msg_util import *
from behave.axob import AXOB
import os

def TEST_axob_SL(date, instrument:int, 
                SecurityIDSource=SecurityIDSource_SZSE, 
                instrument_type=INSTRUMENT_TYPE.STOCK
                ):
    '''TODO: axob save/load'''
    n_max=500

    md_file = f'data/{date}/AX_sbe_szse_{instrument:06d}.log'
    if not os.path.exists(md_file):
        raise f"{md_file} not exists"

    axob_save = AXOB(instrument, SecurityIDSource, instrument_type)
    save_data = None
    axob_load = AXOB(instrument, SecurityIDSource, instrument_type)

    n = 0
    boc = 0
    for msg in axsbe_file(md_file):
        if msg.TradingPhaseMarket==TPM.OpenCall and boc==0:
            boc = 1
            print('openCall start')

        if msg.TradingPhaseMarket>TPM.OpenCall:
            print(f'openCall over, n={n}')
            break
        axob_save.onMsg(msg)
        n += 1
        if n==n_max//2:
            save_data = axob_save.save()
            print(f'save at {n}')
        if n>=n_max:
            print(f'nb over, n={n} saved')
            break
        
    axob_save.are_you_ok()

    axob_load.load(save_data)
    n = 0
    for msg in axsbe_file(md_file):
        if msg.TradingPhaseMarket>TPM.OpenCall:
            print(f'openCall over, n={n}')
            break
        n += 1
        if n==n_max//2:
            print(f'load at {n}')
        if n>n_max//2:
            axob_load.onMsg(msg)
        if n>=n_max:
            print(f'nb over, n={n} saved')
            break

    f_save = axob_save.last_snap
    f_load = axob_load.last_snap

    assert str(f_save)==str(f_load)

    print("TEST_axob_SL done")
    return


@timeit
def TEST_axob_openCall(date, instrument:int, n_max=500, 
                        SecurityIDSource=SecurityIDSource_SZSE, 
                        instrument_type=INSTRUMENT_TYPE.STOCK
                    ):
    md_file = f'data/{date}/AX_sbe_szse_{instrument:06d}.log'
    if not os.path.exists(md_file):
        raise f"{md_file} not exists"

    axob = AXOB(instrument, SecurityIDSource, instrument_type)

    n = 0
    boc = 0
    for msg in axsbe_file(md_file):
        if msg.TradingPhaseMarket==TPM.OpenCall and boc==0:
            boc = 1
            print('openCall start')

        if msg.TradingPhaseMarket>TPM.OpenCall:
            print(f'openCall over, n={n}')
            break
        axob.onMsg(msg)
        n += 1
        if n_max>0 and n>=n_max:
            print(f'nb over, n={n}')
            break
        
    axob.are_you_ok()

    print("TEST_axob_openCall done")
    return


@timeit
def TEST_axob_openCall_bat(source_file, instrument_list:list, n_max=500, 
                            SecurityIDSource=SecurityIDSource_SZSE, 
                            instrument_type=INSTRUMENT_TYPE.STOCK
                            ):
    if not os.path.exists(source_file):
        raise f"{source_file} not exists"

    axobs = {}
    for x in instrument_list:
        axobs[x] = AXOB(x, SecurityIDSource, instrument_type)

    n = 0 #只计算在 instrument_list 内的消息
    boc = 0
    for msg in axsbe_file(source_file):
        if msg.TradingPhaseMarket==TPM.OpenCall and boc==0:
            boc = 1
            print('openCall start')
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

