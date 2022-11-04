# -*- coding: utf-8 -*-

from behave.axob import INSTRUMENT_TYPE
from tool.axsbe_base import SecurityIDSource_SZSE, TPM
from tool.test_util import *
from tool.msg_util import *
from behave.axob import AXOB


def TEST_axob_SL():
    '''TODO: axob save/load'''
    pass


@timeit
def TEST_axob_openCall(date, instrument:int, n_max=500):
    md_file = f'data/{date}/AX_sbe_szse_{instrument:06d}.log'

    axob = AXOB(instrument, SecurityIDSource_SZSE, INSTRUMENT_TYPE.STOCK)

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

