# -*- coding: utf-8 -*-

from datetime import datetime
from time import sleep
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


def TEST_mu_SL(source_file, instrument_list, 
                SecurityIDSource=SecurityIDSource_SZSE, 
                instrument_type=INSTRUMENT_TYPE.STOCK
                ):
    '''TODO: axob save/load'''
    msg_n_max=315
    msg_n_save = 80

    if not os.path.exists(source_file):
        raise f"{source_file} not exists"

    mu_save = MU(instrument_list, SecurityIDSource, instrument_type)
    save_data = None

    n = 0
    boc = 0
    saved =0
    for msg in axsbe_file(source_file):
        if msg.TradingPhaseMarket==TPM.OpenCall and boc==0:
            boc = 1
            print('openCall start')

        if msg.TradingPhaseMarket>TPM.OpenCall:
            print(f'openCall over, n={n}, mu.msg_nb={mu_save.msg_nb}')
            break
        mu_save.onMsg(msg)
        n += 1
        if mu_save.msg_nb==msg_n_save and saved==0:
            save_data = mu_save.save()
            saved = 1
            n_save = n
            print(f'save at {n}')
        if mu_save.msg_nb>=msg_n_max:
            print(f'nb over, n={n} saved')
            n_max = n
            break
    mu_save.are_you_ok()

    pickle.dump(save_data,open("log/test.pkl",'wb'))
    load_data = pickle.load(open("log/test.pkl",'rb'))

    mu_load = MU(instrument_list, SecurityIDSource, instrument_type, load_data=load_data)

    n = 0
    for msg in axsbe_file(source_file):
        if msg.TradingPhaseMarket>TPM.OpenCall:
            print(f'openCall over, n={n}')
            break
        n += 1
        if n==n_save:
            print(f'load at {n}')
        if n>n_save:
            mu_load.onMsg(msg)
        if n>=n_max:
            print(f'nb over, n={n} saved')
            break
    mu_load.are_you_ok()

    f_data_save = mu_save.save()
    pickle.dump(f_data_save,open("log/f_data_save.pkl",'wb'))

    f_data_load = mu_load.save()
    pickle.dump(f_data_load,open("log/f_data_load.pkl",'wb'))
    #.pkl should be binary-same.

    # with open('log/f_data_save.json', 'w') as f: # not real json
    #     f.write(str(f_data_save))

    # with open('log/f_data_load.json', 'w') as f: # not real json
    #     f.write(str(f_data_load))
    assert str(f_data_save)==str(f_data_load)

    print("TEST_mu_SL done")
    return


@timeit
def TEST_axob_bat(source_file, instrument_list:list, n_max=500, 
                    openCall_only=False,
                    SecurityIDSource=SecurityIDSource_SZSE, 
                    instrument_type=INSTRUMENT_TYPE.STOCK,
                    HHMMSSms_max=None,
                    logPack=(print, print, print, print)
                ):
    if not os.path.exists(source_file):
        raise f"{source_file} not exists"

    DBG, INFO, WARN, ERR = logPack

    mu = MU(instrument_list, SecurityIDSource, instrument_type)
    print(f'{datetime.today()} instrumen_nb={len(instrument_list)}, current memory usage={getMemUsageGB():.3f} GB')

    n = 0 #只计算在 instrument_list 内的消息
    n_bgn = 0
    boc = 0
    ecc = 0
    t_bgn = time()
    t_pf = t_bgn
    profile_memUsage = 0
    profile_memFree = getMemFreeGB()
    for msg in axsbe_file(source_file):
        if msg.TradingPhaseMarket==TPM.OpenCall and boc==0:
            boc = 1
            print(f'{datetime.today()} openCall start')

        if msg.TradingPhaseMarket==TPM.Ending and ecc==0:
            ecc = 1
            print(f'{datetime.today()} closeCall over')

        mu.onMsg(msg)
        n += 1
        if n_max>0 and n>=n_max:
            print(f'{datetime.today()} nb over, n={n}')
            break

        if (openCall_only and msg.HHMMSSms>92600000) or \
           (msg.HHMMSSms>150100000):
            print(f'{datetime.today()} Ending: over, n={n}')
            break

        if HHMMSSms_max is not None and HHMMSSms_max>0 and msg.HHMMSSms>HHMMSSms_max:
            print(f'{datetime.today()} HHMMSSms_max: over, n={n}, msg @({msg.TransactTime})')
            break

        now = time()

        if now > t_pf+30: #内存占用采样周期30s
            memUsage = getMemUsageGB()
            if memUsage>profile_memUsage:
                profile_memUsage = memUsage
            memFree = getMemFreeGB()
            if memFree<profile_memFree:
                profile_memFree = memFree
            t_pf = now

            if now>t_bgn+60*10:#内存情况，报告周期10min
                print(f'{datetime.today()} current memory usage={memUsage:.3f} GB free={memFree:.3f} GB'
                    f'(epoch peak={profile_memUsage:.3f} GB, minFree={profile_memFree:.3f} GB),' 
                    f' @{msg.HHMMSSms}')
                t_bgn = now
                profile_memUsage = 0
                profile_memFree = memFree

    if WARN is not None:
        WARN(mu) #保证能记录到文件中
    assert mu.are_you_ok()
    print(f'== TEST_axob_bat PASS ==')
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

    mu = MU([instrument], SecurityIDSource, instrument_type)

    if begin_section is None:
        boc = 0
        HHMMSSms = 0
        section = None
    else:
        section = pickle.load(open(f"log/rolling/{begin_section}.pkl",'rb'))
        mu.load(section['save_data'])
        boc = section['boc']
        HHMMSSms = section['HHMMSSms']
        assert date==section['date'] and instrument==section['instrument'] and (n_max==0 or n_max>section['n'])

    n = 0
    for msg in axsbe_file(md_file):
        if section is not None and n<section['n']:
            n += 1
            continue

        if msg.TradingPhaseMarket==TPM.OpenCall and boc==0:
            boc = 1
            print('openCall start')

        # if msg.TradingPhaseMarket==TPM.PreTradingBreaking and signal_oce==0:    # 消息状态切换，触发信号
        #     signal_oce = 1
        #     axob.onMsg(AX_SIGNAL.OPENCALL_END)
        # if msg.TradingPhaseMarket==TPM.Breaking and signal_amte==0:    # 消息状态切换，触发信号
        #     signal_amte = 1
        #     axob.onMsg(AX_SIGNAL.AMTRADING_END)
        # if msg.TradingPhaseMarket==TPM.CloseCall and signal_pmte==0:    # 消息状态切换，触发信号
        #     signal_pmte = 1
        #     axob.onMsg(AX_SIGNAL.PMTRADING_END)
        # if msg.TradingPhaseMarket==TPM.Ending:
        #     axob.onMsg(AX_SIGNAL.ALL_END)

        mu.onMsg(msg)
        n += 1
        if n_max>0 and n>=n_max:
            print(f'nb over, n={n}')
            break

        if HHMMSSms==0 or boc==0:
            HHMMSSms=msg.HHMMSSms
        else:
            if msg.HHMMSSms > HHMMSSms + rolling_gap*100000:    # step = gap * 1min
                HHMMSSms = msg.HHMMSSms
                save_data = mu.save()
                section = {
                    'save_data':save_data,
                    'date':date,
                    'instrument':instrument,
                    'n_max':n_max,
                    'boc':boc,
                    'n':n,
                    'HHMMSSms':HHMMSSms,
                }
                section_name = f'{date}_{instrument:06d}_{n_max}_{rolling_gap}_{HHMMSSms}'
                pickle.dump(section, open(f"log/rolling/{section_name}.pkl",'wb'))
                print(f'saved section={section_name}')

        if msg.TradingPhaseMarket==TPM.Ending and msg.HHMMSSms>150100000:
            print(f'Ending: over, n={n}')
            break
    print(mu)
    if isTPMfreeze(mu):
        assert mu.are_you_ok()

    print("TEST_axob_rolling PASS")
    return



@timeit
def TEST_mu_rolling(source_file, instrument_list, n_max=500, rolling_gap=5,
                        begin_section=None,
                        SecurityIDSource=SecurityIDSource_SZSE, 
                        instrument_type=INSTRUMENT_TYPE.STOCK,
                        HHMMSSms_max=None
                    ):
    '''
    begin_section=None:滚动保存现场，现场名称将打印在终端
    begin_section='现场名称':装载保存的现场并继续测试
	rolling_gap:保存间隔，以分钟为单位
    '''
    if not os.path.exists(source_file):
        raise f"{source_file} not exists"

    mu = MU(instrument_list, SecurityIDSource, instrument_type)

    if begin_section is None:
        boc = 0
        HHMMSSms = 0
        section = None
        skip_nb = 0
    else:
        section = pickle.load(open(f"log/rolling/{begin_section}.pkl",'rb'))
        mu.load(section['save_data'])
        boc = section['boc']
        HHMMSSms = section['HHMMSSms']
        skip_nb = section['n']
        assert source_file==section['source_file'] and instrument_list==section['instrument_list'] and (n_max==0 or n_max>section['n'])

    n = 0
    for msg in axsbe_file(source_file, 0):
        if section is not None and n<section['n']:
            n += 1
            continue

        if msg.TradingPhaseMarket>=TPM.OpenCall and boc==0:
            boc = 1
            print('openCall start')

        mu.onMsg(msg)
        n += 1
        if n_max>0 and n>=n_max:
            print(f'nb over, n={n}')
            break

        if HHMMSSms==0 or boc==0:
            HHMMSSms=msg.HHMMSSms
        else:
            if msg.HHMMSSms > HHMMSSms + rolling_gap*100000:    # step = gap * 1min
                HHMMSSms = msg.HHMMSSms
                save_data = mu.save()
                section = {
                    'save_data':save_data,
                    'source_file':source_file,
                    'instrument_list':instrument_list,
                    'n_max':n_max,
                    'boc':boc,
                    'n':n,
                    'HHMMSSms':HHMMSSms,
                }
                section_name = f'mu_{rolling_gap}_{HHMMSSms}'
                pickle.dump(section, open(f"log/rolling/{section_name}.pkl",'wb'))
                print(f'saved section={section_name}')

        if msg.TradingPhaseMarket==TPM.Ending and msg.HHMMSSms>150100000:
            print(f'Ending: over, n={n}')
            break

        if HHMMSSms_max is not None and HHMMSSms_max>0 and HHMMSSms>HHMMSSms_max:
            print(f'HHMMSSms_max: over, n={n}, msg @({msg.TransactTime})')
            break


    print(mu)
    if isTPMfreeze(mu):
        assert mu.are_you_ok()

    print("TEST_axob_rolling PASS")
    return


@timeit
def TEST_mu_bat(source_file, instrument_list:list,
                batch_nb,
                bgn_batch=0,
                SecurityIDSource=SecurityIDSource_SZSE, 
                instrument_type=INSTRUMENT_TYPE.STOCK,
                logPack=(print, print, print, print)
                ):
    '''
    将instrument_list分组到多个mu进行测试，减少内存占用。
    instrument_list: 分组前的标的列表，输入时尽量按照逐笔数目排序，有利于分组均衡
    batch_nb:分成几组。 若分为n组，则每组序号为：[0, n, 2n...], [1, n+1, 2n+1...] ... [n-1, 2n-1, 3n-1...]
    bgn_batch:从第几分组开始运行，取值范围:[0, batch_nb-1].
    '''
    for i in range(bgn_batch, batch_nb):
        current_list = instrument_list[i::batch_nb]
        freeGB = getMemFreeGB()
        print(f'{datetime.today()} Working on batch {i}/{batch_nb}, current system free memory={freeGB:.3f} GB...')
        while freeGB*168<len(current_list)*30:  #168只个股最大约占30G
            print(f'{datetime.today()} sleep for not enough free memory...')
            sleep(180)
            freeGB = getMemFreeGB()
            print(f'{datetime.today()} current system free memory={freeGB:.3f} GB' 
                  f'(each instrument={freeGB/len(current_list):.4f}, require={20/168*len(current_list):.4f})')
        TEST_axob_bat(source_file, current_list, n_max=0, openCall_only=False, SecurityIDSource=SecurityIDSource, instrument_type=instrument_type, logPack=logPack) #
