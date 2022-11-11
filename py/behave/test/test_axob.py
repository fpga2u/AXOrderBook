# -*- coding: utf-8 -*-

from tool.axsbe_base import SecurityIDSource_SZSE, TPM, INSTRUMENT_TYPE
from tool.test_util import *
from tool.msg_util import *
from behave.mu import *
import os
import pickle

def TEST_axob_SL(date, instrument:int, 
                SecurityIDSource=SecurityIDSource_SZSE, 
                instrument_type=INSTRUMENT_TYPE.STOCK
                ):
    '''TODO: axob save/load'''
    n_max=31500
    n_save = 800

    md_file = f'data/{date}/AX_sbe_szse_{instrument:06d}.log'
    if not os.path.exists(md_file):
        raise f"{md_file} not exists"

    axob_save = AXOB(instrument, SecurityIDSource, instrument_type)
    save_data = None

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
        if n==n_save:
            save_data = axob_save.save()
            print(f'save at {n}')
        if n>=n_max:
            print(f'nb over, n={n} saved')
            break
    axob_save.are_you_ok()

    pickle.dump(save_data,open("log/test.pkl",'wb'))
    load_data = pickle.load(open("log/test.pkl",'rb'))

    axob_load = AXOB(instrument, SecurityIDSource, instrument_type)
    axob_load.load(load_data)
    n = 0
    for msg in axsbe_file(md_file):
        if msg.TradingPhaseMarket>TPM.OpenCall:
            print(f'openCall over, n={n}')
            break
        n += 1
        if n==n_save:
            print(f'load at {n}')
        if n>n_save:
            axob_load.onMsg(msg)
        if n>=n_max:
            print(f'nb over, n={n} saved')
            break
    axob_load.are_you_ok()

    last_snap_save = axob_save.last_snap
    last_snap_load = axob_load.last_snap
    assert str(last_snap_save)==str(last_snap_load)

    print(f'axob_save.rebuilt_snaps={len(axob_save.rebuilt_snaps)}; axob_load.rebuilt_snaps={len(axob_load.rebuilt_snaps)}')
    assert len(axob_save.rebuilt_snaps)==len(axob_load.rebuilt_snaps)
    print(f'axob_save.market_snaps={len(axob_save.market_snaps)}; axob_load.market_snaps={len(axob_load.market_snaps)}')
    assert len(axob_save.market_snaps)==len(axob_load.market_snaps)
    print(f'axob_save.rebuilt_snaps={len(axob_save.rebuilt_snaps)}; axob_load.rebuilt_snaps={len(axob_load.rebuilt_snaps)}')
    assert len(axob_save.order_map)==len(axob_load.order_map)
    assert len(axob_save.bid_level_tree)==len(axob_load.bid_level_tree)
    assert len(axob_save.ask_level_tree)==len(axob_load.ask_level_tree)

    f_data_save = axob_save.save()
    pickle.dump(f_data_save,open("log/f_data_save.pkl",'wb'))

    f_data_load = axob_load.save()
    pickle.dump(f_data_load,open("log/f_data_load.pkl",'wb'))
    #.pkl should be binary-same.

    # with open('log/f_data_save.json', 'w') as f: # not real json
    #     f.write(str(f_data_save))

    # with open('log/f_data_load.json', 'w') as f: # not real json
    #     f.write(str(f_data_load))
    assert str(f_data_save)==str(f_data_load)

    print("TEST_axob_SL done")
    return



@timeit
def TEST_axob_bat(source_file, instrument_list:list, n_max=500, 
                    openCall_only=False,
                    SecurityIDSource=SecurityIDSource_SZSE, 
                    instrument_type=INSTRUMENT_TYPE.STOCK
                ):
    if not os.path.exists(source_file):
        raise f"{source_file} not exists"

    mu = MU(instrument_list, SecurityIDSource, instrument_type)

    n = 0 #只计算在 instrument_list 内的消息
    boc = 0
    ecc = 0
    for msg in axsbe_file(source_file):
        if msg.TradingPhaseMarket==TPM.OpenCall and boc==0:
            boc = 1
            print('openCall start')

        if msg.TradingPhaseMarket==TPM.Ending and ecc==0:
            ecc = 1
            print(f'closeCall over')

        mu.onMsg(msg)
        n += 1
        if n_max>0 and n>=n_max:
            print(f'nb over, n={n}')
            break

        if (openCall_only and msg.HHMMSSms>92600000) or \
           (msg.HHMMSSms>150100000):
            print(f'Ending: over, n={n}')
            break

    assert mu.are_you_ok()
    print("TEST_axob_bat PASS")
    return


def TEST_axob(date, instrument:int, n_max=500, 
                openCall_only=False,
                SecurityIDSource=SecurityIDSource_SZSE, 
                instrument_type=INSTRUMENT_TYPE.STOCK
            ):
    md_file = f'data/{date}/AX_sbe_szse_{instrument:06d}.log'
    if not os.path.exists(md_file):
        raise f"{md_file} not exists"

    TEST_axob_bat(md_file, [instrument], n_max, openCall_only, SecurityIDSource, instrument_type)

    return


@timeit
def TEST_axob_rolling(date, instrument:int, n_max=500, rolling_gap=5,
                        begin_section=None,
                        SecurityIDSource=SecurityIDSource_SZSE, 
                        instrument_type=INSTRUMENT_TYPE.STOCK
                    ):
    '''
    begin_section=None:滚动保存现场，现场名称将打印在终端
    begin_section='现场名称':装载保存的现场并继续测试
	rolling_gap:保存间隔，以分钟为单位
    '''
    md_file = f'data/{date}/AX_sbe_szse_{instrument:06d}.log'
    if not os.path.exists(md_file):
        raise f"{md_file} not exists"

    axob = AXOB(instrument, SecurityIDSource, instrument_type)

    if begin_section is None:
        boc = 0
        signal_oce = 0
        signal_amte = 0
        HHMMSSms = 0
        section = None
    else:
        section = pickle.load(open(f"log/rolling/{begin_section}.pkl",'rb'))
        axob.load(section['save_data'])
        boc = section['boc']
        signal_oce = section['signal_oce']
        signal_amte = section['signal_amte']
        signal_pmte = section['signal_pmte']
        HHMMSSms = section['HHMMSSms']
        assert date==section['date'] and instrument==section['instrument'] and (n_max==0 or n_max>section['n'])

    signal_pmte = 0
    n = 0
    for msg in axsbe_file(md_file):
        if section is not None and n<section['n']:
            n += 1
            continue

        if msg.TradingPhaseMarket==TPM.OpenCall and boc==0:
            boc = 1
            print('openCall start')

        if msg.TradingPhaseMarket==TPM.PreTradingBreaking and signal_oce==0:    # 消息状态切换，触发信号
            signal_oce = 1
            axob.onMsg(AX_SIGNAL.OPENCALL_END)
        if msg.TradingPhaseMarket==TPM.Breaking and signal_amte==0:    # 消息状态切换，触发信号
            signal_amte = 1
            axob.onMsg(AX_SIGNAL.AMTRADING_END)
        if msg.TradingPhaseMarket==TPM.CloseCall and signal_pmte==0:    # 消息状态切换，触发信号
            signal_pmte = 1
            axob.onMsg(AX_SIGNAL.PMTRADING_END)
        if msg.TradingPhaseMarket==TPM.Ending:
            axob.onMsg(AX_SIGNAL.ALL_END)

        axob.onMsg(msg)
        n += 1
        if n_max>0 and n>=n_max:
            print(f'nb over, n={n}')
            break

        if HHMMSSms==0 or boc==0:
            HHMMSSms=msg.HHMMSSms
        else:
            if msg.HHMMSSms > HHMMSSms + rolling_gap*100000:    # step = gap * 1min
                HHMMSSms = msg.HHMMSSms
                save_data = axob.save()
                section = {
                    'save_data':save_data,
                    'date':date,
                    'instrument':instrument,
                    'n_max':n_max,
                    'boc':boc,
                    'signal_oce':signal_oce,
                    'signal_amte':signal_amte,
                    'signal_pmte':signal_pmte,
                    'n':n,
                    'HHMMSSms':HHMMSSms,
                }
                section_name = f'{date}_{instrument:06d}_{n_max}_{rolling_gap}_{HHMMSSms}'
                pickle.dump(section, open(f"log/rolling/{section_name}.pkl",'wb'))
                print(f'saved section={section_name}')

        if msg.TradingPhaseMarket==TPM.Ending and msg.HHMMSSms>150100000:
            print(f'Ending: over, n={n}')
            break
    print(axob)
    if isTPMfreeze(axob):
        assert axob.are_you_ok()

    print("TEST_axob_rolling PASS")
    return
