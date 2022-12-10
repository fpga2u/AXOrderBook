# -*- coding: utf-8 -*-

import binaryTree.AVLTree as AVL
import binaryTree.RBTree as RB
import binaryTree.AVLTree_wr as AVL_wr
from binaryTree.util import *
import random
from random import shuffle, randint
import os
import sys
import time

from tool.test_util import timeit

TYPE_MAP = {
    'AVL':{'TREE':AVL.AVLTree, 'NODE':AVL.AVLTNode, 'LOGGER':AVL.AVLTree_logger},
    'AVL_wr':{'TREE':AVL_wr.AVLTree, 'NODE':AVL_wr.AVLTNode, 'LOGGER':AVL_wr.AVLTree_logger},
    'RB':{'TREE':RB.RBTree, 'NODE':RB.RBTNode, 'LOGGER':RB.RBTree_logger},
}


def _insert_then_remove(l:list, s, type, debug_level=2):
    if not os.path.exists(DBG_VIEW_ROOT):
        os.makedirs(DBG_VIEW_ROOT, exist_ok=True)

    assert type in TYPE_MAP, f'unkown tree type={type}!'

    TREE = TYPE_MAP[type]['TREE']
    NODE = TYPE_MAP[type]['NODE']
    LOGGER = TYPE_MAP[type]['LOGGER']

    t = TREE(s, debug_level=debug_level)
    for n in l:
        new_node = NODE(n)
        t.insert(new_node, auto_rebalance=True)
    t.debugShow(label='insert_final')

    LOGGER.info(t.inorder_list_inc())
    LOGGER.info(t.inorder_list_dec())

    minV, midV, maxV = min(l), l[len(l)//2], max(l)
    assert t.locate(minV-1)==None
    assert t.locate(minV).value==minV
    assert t.locate(midV).value==midV
    assert t.locate(maxV).value==maxV
    assert t.locate(maxV+1)==None
    assert t.locate_min().value==minV
    assert t.locate_max().value==maxV
    LOGGER.info(f'locate({midV}) = {t.locate(midV)}')
    LOGGER.info(f'locate({maxV+1}) = {t.locate(maxV+1)}')
    LOGGER.info(f'locate({minV-1}) = {t.locate(minV-1)}')
    LOGGER.info(f'locate_min = {t.locate_min()}')
    LOGGER.info(f'locate_max = {t.locate_max()}')
    LOGGER.info(f'locate_lower({midV}) = {t.locate_lower(t.locate(midV))}')
    LOGGER.info(f'locate_higher({midV}) = {t.locate_higher(t.locate(midV))}')

    LOGGER.info('\n'+t.printTree())

    for _ in range(min(len(l)//3, 3)):
        rootV = t.getRoot().value
        LOGGER.info(f'rootV = {rootV}')
        t.remove(rootV, auto_rebalance=True)
        l.remove(rootV)

    for n in l:
        t.remove(n, auto_rebalance=True)
    t.debugShow(label='remove_final')
    LOGGER.info(f'profile:\n{t.profile()}')

def _save_load(type):
    '''
    测试：导出/导入树
    '''
    if not os.path.exists(DBG_VIEW_ROOT):
        os.makedirs(DBG_VIEW_ROOT, exist_ok=True)
    assert type in TYPE_MAP, f'unkown tree type={type}!'

    TREE = TYPE_MAP[type]['TREE']
    NODE = TYPE_MAP[type]['NODE']
    LOGGER = TYPE_MAP[type]['LOGGER']
    l = [14987, 16059, 20287, 23639, 47623, 47624, 47625, 50672, 87188, 87189, 97471, 97472, 118563, 124604, 135780, 135781]
    random.seed(1000)
    shuffle(l)
    t = TREE('before_save', debug_level=2)
    for n in l:
        new_node = NODE(n)
        t.insert(new_node)
    saved = t.save()    #保存旧树结构
    LOGGER.info(saved)
    new_node = NODE(50677)
    t.insert(new_node)  #旧树新增一个节点 50677
    t.debugShow(label="save-final")
    save_final = t.printTree()
    LOGGER.info('\n'+save_final)

    tl = TREE('after_load', debug_level=2)      #新树装载旧树
    tl.load(saved)
    assert(t.size != tl.size)

    saved2 = tl.save()
    LOGGER.info(saved2)
    new_node = NODE(60000)
    tl.insert(new_node) #新树新增一个节点 60000
    tl.debugShow(label="load-final")
    load_final = tl.printTree()
    LOGGER.info('\n'+load_final)

    assert(t.size == tl.size)
    save_final = save_final.replace('50677', '60000')
    assert(save_final==load_final)

def _batch_insert_remove(seed, draw, type, name):
    if not os.path.exists(DBG_VIEW_ROOT):
        os.makedirs(DBG_VIEW_ROOT, exist_ok=True)
    random.seed(seed)
    if draw:
        debug_level = 2
    else:
        debug_level = 0
        
    assert type in TYPE_MAP, f'unkown tree type={type}!'

    TREE = TYPE_MAP[type]['TREE']
    NODE = TYPE_MAP[type]['NODE']
    LOGGER = TYPE_MAP[type]['LOGGER']

    t = TREE(name=name, debug_level=debug_level)

    total_data_size = 30
    batch_nb = 4

    value_list = [x for x in range(total_data_size)]
    shuffle(value_list)
    LOGGER.info(f'{sys._getframe().f_code.co_name} seed={seed} batch_nb={batch_nb} value_list={value_list}')

    ##Create batch insert/remove lists ##
    #for example:
    # insert_lists = [ [8, 10, 1, 3, 11], [6, 15, 0, 12, 16, 2], [14, 5, 19, 9, 13, 17, 4, 7, 18] ]
    # remove_lists = [ [8, 10, 1],        [16, 0, 6, 12, 15],    [9, 5, 13, 17, 4, 14, 19],       [3, 11, 2, 7, 18]]
    insert_lists = []
    bg = 0
    for i in range(batch_nb):
        cl = randint(3, len(value_list)//batch_nb)
        insert_lists.append(value_list[bg: bg+cl])
        bg = bg+cl
    insert_lists.append(value_list[bg:])


    remove_lists = []
    remove_lists_r = []
    for i in range(len(insert_lists)):
        cl = randint(3, len(insert_lists[i]))
        lst_i = insert_lists[i][:cl]
        shuffle(lst_i)
        remove_lists.append(lst_i)
        remove_lists_r.extend(insert_lists[i][cl:])
    remove_lists.append(remove_lists_r)

    LOGGER.info(f'insert_lists={insert_lists}')
    LOGGER.info(f'remove_lists={remove_lists}')

    LOGGER.info(t)
    for n in range(len(insert_lists)):

        list = insert_lists[n]
        LOGGER.info(f"insert list={list}")

        for i in list:
            new_node = NODE(i)
            t.insert(new_node)
            LOGGER.info(t.inorder_list_inc())
            LOGGER.info(t.inorder_list_dec())

        del_list = remove_lists[n]

        LOGGER.info(f"del_list={del_list}")
        for i in del_list:
            t.remove(i)
            LOGGER.info(t.inorder_list_inc())
            LOGGER.info(t.inorder_list_dec())


    del_list = remove_lists[-1]

    LOGGER.info(f"del_list={del_list}")
    for i in del_list:
        t.remove(i)
        LOGGER.info(t.inorder_list_inc())
        LOGGER.info(t.inorder_list_dec())

    LOGGER.info(f'profile:\n{t.profile()}')
    assert t.size==0



def TESTAVL_insert_then_removeA():
    _insert_then_remove([x for x in range(10)], sys._getframe().f_code.co_name, 'AVL', debug_level=1)

def TESTAVL_insert_then_removeB():
    _insert_then_remove([9,8,7,6,5,4,3,2,1], sys._getframe().f_code.co_name, 'AVL', debug_level=1)

def TESTAVL_insert_then_removeC():
    l = [x for x in range(500, 0, -1)]
    random.seed(1110)
    shuffle(l)
    _insert_then_remove(l, sys._getframe().f_code.co_name, 'AVL', debug_level=0)

def TESTAVL_batch_insert_remove(seed, draw):
    _batch_insert_remove(seed, draw, 'AVL', name=sys._getframe().f_code.co_name)

def TESTAVL_save_load():
    _save_load('AVL')

def TESTAVL_no_auto_rebalance(inorder):
    '''
    测试：在插入时不进行平衡
    inorder 插入值是否递增；True: 递增，将退化成链表；False: 插入值随机
    '''
    l = [14987, 16059, 20287, 23639, 47623, 47624, 47625, 50672, 87188, 87189, 97471, 97472, 118563, 124604, 135780, 135781]
    if not inorder:
        random.seed(1000)
        shuffle(l)
    tree_name = 'no_auto_rebalance' + ('(inorder)' if inorder else '(random)')
    t = AVL.AVLTree(tree_name, debug_level=1)
    for n in l:
        new_node = AVL.AVLTNode(n)
        t.insert(new_node, auto_rebalance=False)
    #TODO: 在所有插入完成后平衡，目前不成功
    # t._balance(t.locate_max(t.root), recurve_to_root=True)
    # # t._balance(t.root)
    # t._balance(t.locate_min(t.root), recurve_to_root=True)
    # t.debugShow(save_graph=True)







def TESTRBT_insert_then_removeA():
    _insert_then_remove([x for x in range(10)], sys._getframe().f_code.co_name, 'RB', debug_level=1)

def TESTRBT_insert_then_removeB():
    _insert_then_remove([x for x in range(10,0,-1)], sys._getframe().f_code.co_name, 'RB', debug_level=1)

def TESTRBT_insert_then_removeC():
    _insert_then_remove([4, 6, 3, 1, 7, 9, 8, 5, 2], sys._getframe().f_code.co_name, 'RB', debug_level=1)

def TESTRBT_batch_insert_remove(seed, draw):
    _batch_insert_remove(seed, draw, 'RB', name=sys._getframe().f_code.co_name)

def TESTRBT_save_load():
    _save_load('RB')


def extract_level_access_log(log_file, modify_only, side='both'):
    '''
    抽取日志中的价格档访问消息，独立写入一个新文件，便于观察和测试二叉树。
    与 TESTTree_using_log 配合。
    log_file: TEST_axob 测试日志，示例在 run_test_behave.py 中有，生成前需设置 axob.py 中的 EXPORT_LEVEL_ACCESS 为 True。
    '''
    export_file = log_file+'.la.log'
    with open(log_file, 'r') as f, open(export_file, 'w') as o:
        print(f'export file={export_file}')
        while True:
            l = f.readline()
            if not l:break
            if l.find('LEVEL_ACCESS')<0:
                continue

            if modify_only and l.find(' insert ')<0 and l.find(' remove ')<0:
                continue

            if side=='bid' and l.find(' BID ')<0:
                continue

            if side=='ask' and l.find(' ASK ')<0:
                continue

            o.write(l)
    return export_file

@timeit
def TESTTree_using_log(log_file, tree_type, bid_draw_size=None, ask_draw_size=None):
    '''
    !!!目前只支持单只个股!!!
    读取 extract_level_access_log 输出的日志，构造价格档二叉树。
    log_file: extract_level_access_log 输出的日志文件
    tree_type: 'AVL' or 'RB'
    bid_draw_size: bid树的size大于此值时将绘出树结构并保存到png文件，最大值可以在 extract_level_access_log的【输入】文件末尾查找。
                   None时不输出png。
    ask_draw_size: ask树的size大于此值时将绘出树结构并保存到png文件，最大值可以在 extract_level_access_log的【输入】文件末尾查找。
                   None时不输出png。
    '''
    assert tree_type in TYPE_MAP, f'unkown tree type={tree_type}!'
    TREE = TYPE_MAP[tree_type]['TREE']
    NODE = TYPE_MAP[tree_type]['NODE']
    LOGGER = TYPE_MAP[tree_type]['LOGGER']

    ask = TREE(f'{tree_type}_ASK_')
    bid = TREE(f'{tree_type}_BID_')

    working_tree = {
        'BID':bid,
        'ASK':ask,
    }
    with open(log_file, 'r') as f:
        while True:
            l = f.readline()
            if not l:break

            for cmd in [' remove ', ' insert ', ' locate ', ' writeback ', ' locate_higher ', ' locate_lower ']:
                p = l.find(cmd)
                if p>=0:
                    v = int(l[p:].strip().split(' ')[1])
                    if l.find(' BID ')>0:
                        working_tree = bid
                    elif l.find(' ASK ')>0:
                        working_tree = ask
                    else:
                        continue
                    if cmd==' insert ':
                        new_node = NODE(v)
                        working_tree.insert(new_node)
                    elif cmd==' remove ':
                        working_tree.remove(v)
                    elif cmd==' locate ':
                        working_tree.locate(v)
                    elif cmd==' writeback ':
                        working_tree.dmy_writeback()
                    elif cmd==' locate_higher ':
                        working_tree.locate_higher(working_tree.locate(v))
                    elif cmd==' locate_lower ':
                        working_tree.locate_lower(working_tree.locate(v))

                    if bid_draw_size is not None and bid.size >= bid_draw_size:
                        bid.debugShow('max_size', force_draw=1)

                    if ask_draw_size is not None and ask.size >= ask_draw_size:
                        ask.debugShow('max_size', force_draw=1)
                    break

    LOGGER.info(f'ASK max size={ask.size_max}')
    LOGGER.info(f'ASK.profile:\n{ask.profile()}')
    LOGGER.info(f'BID max size={bid.size_max}')
    LOGGER.info(f'BID.profile:\n{bid.profile()}')



def TESTAVLWR_insert_then_removeA():
    l = [x for x in range(10)]
    _insert_then_remove(l, sys._getframe().f_code.co_name, 'AVL_wr', debug_level=1)

def TESTAVLWR_insert_then_removeB():
    l = [x for x in range(9, 0, -1)]
    _insert_then_remove(l, sys._getframe().f_code.co_name, 'AVL_wr', debug_level=1)

def TESTAVLWR_insert_then_removeC():
    l = [x for x in range(500, 0, -1)]
    LOGGER = TYPE_MAP['AVL_wr']['LOGGER']
    random.seed(1110)
    shuffle(l)
    _insert_then_remove(l, sys._getframe().f_code.co_name, 'AVL_wr', debug_level=0)
    
def TESTAVLWR_batch_insert_remove(seed, draw):
    _batch_insert_remove(seed, draw, 'AVL_wr', name=sys._getframe().f_code.co_name)

def TESTAVLWR_save_load():
    _save_load('AVL_wr')
