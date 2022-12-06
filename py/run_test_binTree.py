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

    ### test VAL
    # binTree.TESTAVL_insert_then_removeA()
    # binTree.TESTAVL_insert_then_removeB()
    # binTree.TESTAVL_insert_then_removeC()
    # binTree.TESTAVL_batch_insert_remove(671, True)
    # for i in range(10):
    #     binTree.TESTAVL_batch_insert_remove(i*7+13, False)
    # binTree.TESTAVL_save_load()
    # binTree.TESTAVL_no_auto_rebalance(True)
    # binTree.TESTAVL_no_auto_rebalance(False)

    # ### RBTree
    # binTree.TESTRBT_insert_then_removeA()
    # binTree.TESTRBT_insert_then_removeB()
    # binTree.TESTRBT_insert_then_removeC()
    # binTree.TESTRBT_batch_insert_remove(671, True)
    # for i in range(10):
    #     binTree.TESTRBT_batch_insert_remove(i*7+13, False)

    # binTree.TESTAVLWR_insert_then_removeA()
    # binTree.TESTAVLWR_insert_then_removeB()
    # binTree.TESTAVLWR_insert_then_removeC()

    # ### 根据个股增、删价格档日志，测试不同二叉树的行为
    tree_log = binTree.extract_level_access_log('log/301336_220812_LEVEL_ACCESS.log', modify_only=True, side='both')
    # binTree.TESTTree_using_log(tree_log, 'AVL', 450, 510)
    # binTree.TESTTree_using_log(tree_log, 'RB', 450, 510)
    binTree.TESTTree_using_log(tree_log, 'AVL_wr', 450, 510)
