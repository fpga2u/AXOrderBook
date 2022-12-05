# -*- coding: utf-8 -*-

import traceback
import logging
import datetime
from time import localtime
import os
import behave.test.test_axob as behave
from tool.axsbe_base import INSTRUMENT_TYPE, SecurityIDSource_SZSE
import tool.test.test_msg as msg

if __name__== '__main__':
    myname = os.path.split(__file__)[1][:-3]
    mytime = str(datetime.datetime(*localtime()[:6])).replace(':',"").replace('-',"").replace(" ","_")

    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(f'log/{myname}_{mytime}.log')
    # fh = logging.FileHandler(f'log/{myname}.log', mode='w')
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

    ###测试20220815所有有委托的只股票，全天
    data_source = "H:/AXOB_data_newP_ru/20220815/sbe_20220815_all.log"
    logger.info('TEST_print_securityID')
    all_inc, min_inc, max_inc = msg.TEST_print_securityID(data_source, read_nb=0, instrument_type=INSTRUMENT_TYPE.STOCK)
    print(f'all_inc len={len(all_inc)}')

    logger.info('starting TEST_axob_bat')
    fh.setLevel(logging.INFO)
    sh.setLevel(logging.ERROR)
    try:
        behave.TEST_mu_bat(data_source, all_inc, batch_nb=16, bgn_batch=0, SecurityIDSource=SecurityIDSource_SZSE, instrument_type=INSTRUMENT_TYPE.STOCK, logPack=logPack) #
    except Exception as e:
        logger.error(f'{traceback.format_exc()}')
