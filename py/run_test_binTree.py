# -*- coding: utf-8 -*-

import logging
import datetime
from time import localtime
import os
import binaryTree.test.test_binTree as binTree

if __name__== '__main__':
    myname = os.path.split(__file__)[1][:-3]
    mytime = str(datetime.datetime(*localtime()[:6])).replace(':',"").replace('-',"").replace(" ","_")

    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)

    # fh = logging.FileHandler(f'log/{myname}_{mytime}.log')
    fh = logging.FileHandler(f'log/{myname}.log', mode='w')
    fh.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)

    formatter_ts = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter_nts = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter_nts)
    sh.setFormatter(formatter_ts)

    logger.addHandler(fh)
    logger.addHandler(sh)

    binTree.TESTAVL_insert_then_removeA()
    # binTree.TESTAVL_insert_then_removeB()
    # binTree.TESTAVL_insert_then_removeC()
    # binTree.TESTAVL_batch_insert_remove()
    # binTree.TESTAVL_save_load()
    # binTree.test_pattern_no_auto_rebalance()
