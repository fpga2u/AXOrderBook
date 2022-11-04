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

    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info('starting TEST_axob_openCall')
    behave.TEST_axob_openCall(20220422, 1, 13500)

    logger.info('starting TEST_axob_openCall')
    behave.TEST_axob_openCall(20220425, 2594, 13621)

    logger.info('starting TEST_axob_openCall')
    behave.TEST_axob_openCall(20220426, 300750, 13621)


