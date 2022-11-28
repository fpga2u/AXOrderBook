# -*- coding: utf-8 -*-

import logging
import datetime
from time import localtime
import os
import behave.test.test_axob as behave

if __name__== '__main__':
    myname = os.path.split(__file__)[1][:-3]
    mytime = str(datetime.datetime(*localtime()[:6])).replace(':',"").replace('-',"").replace(" ","_")

    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)

    # fh = logging.FileHandler(f'log/{myname}_{mytime}.log')
    fh = logging.FileHandler(f'log/{myname}.log', mode='w')
    fh.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setLevel(logging.WARNING)

    formatter_ts = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter_nts = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter_nts)
    sh.setFormatter(formatter_ts)

    logger.addHandler(fh)
    logger.addHandler(sh)
    logPack = logger.debug, logger.info, logger.warn, logger.error

    ### 20220617测试错误
    # logger.info('starting TEST_axob_bat')
    # data_source = "data/20220617/bat_test2.log"
    # ptn=[301129]
    # behave.TEST_axob_bat(data_source, ptn, n_max=0, openCall_only=False, logPack=logPack) #
    
    # ### 20220609测试错误
    # logger.info('starting TEST_axob_bat')
    # behave.TEST_axob(20220609, 301160, 0) #收盘集合竞价时无价格档在笼子外
    
    # ### 20220622测试错误
    # logger.info('starting TEST_axob_bat')
    # behave.TEST_axob(20220622, 300103, 0)

    # ### 20220623测试错误
    # logger.info('starting TEST_axob_bat')
    # behave.TEST_axob(20220623, 300928, 0) #买方价格笼子外订单连续进入撮合直到涨停，导致买方本方最优价过期却被用作买方参考价。

    ### 20221010测试错误
    # logger.info('starting TEST_axob_bat')
    # behave.TEST_axob(20221010, 301313, 0)

    #########
    # logger.info('starting TEST_axob_SL')
    # behave.TEST_axob_SL(20220422, 1)
    
    # logger.info('starting TEST_mu_SL')
    # data_source = "data/20221010/sbe_20221010_all.log"
    # # min_inc=[200054, 200512, 200030, 200045, 200553, 200011, 200020, 200530, 200025, 300996, 200028, 200152, 301059, 200706, 200550, 200037, 200521, 200505, 200056, 300354, 300930, 301066, 300980, 200029, 200055, 300508, 200019, 200026, 300668, 2569, 200992, 200017, 200761, 300870, 2485, 2870, 200570, 301072, 200581, 200413, 300733, 300069, 300654, 201872, 300916, 200771, 2857, 972, 200541, 200058, 2972, 301099, 300530, 301004, 504, 300757, 2735, 300645, 2692, 300948, 200016, 2200, 300885, 2058, 200468, 300833, 300622, 301239, 200726, 300876, 301106, 2975, 200429, 301057, 300550, 300897, 300791, 300521, 2779, 300892, 300964, 301097, 300489, 300984, 300523, 300971, 300426, 300779, 300515, 301020, 301049, 300816, 300958, 300982, 300715, 300986, 2724, 301012, 301182, 300417]
    # min_inc=[300668, 300996, 301059, 1]
    # behave.TEST_mu_SL(data_source, min_inc) #
