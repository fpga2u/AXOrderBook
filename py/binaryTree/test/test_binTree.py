# -*- coding: utf-8 -*-

from binaryTree.AVLTree import *
from binaryTree.RBTree import *
import random
from random import shuffle, randint
import os
import sys

def _AVL_insert_then_remove(l, s):
    if not os.path.exists(DBG_VIEW_ROOT):
        os.makedirs(DBG_VIEW_ROOT, exist_ok=True)

    t = AVLTree(s, 1)
    for n in l:
        new_node = AVLTNode(n, host_tree=t)
        t.insert(new_node, auto_rebalance=True)
    t.debugShow(label='insert_final')

    AVLTree_logger.info(t.inorder_list_inc())
    AVLTree_logger.info(t.inorder_list_dec())

    AVLTree_logger.info(f'locate({l[len(l)//2]}) = {t.locate(l[len(l)//2])}')
    AVLTree_logger.info(f'locate({max(l)+1}) = {t.locate(max(l)+1)}')
    AVLTree_logger.info(f'locate({min(l)-1}) = {t.locate(min(l)-1)}')
    AVLTree_logger.info(f'locate_min = {t.locate_min()}')
    AVLTree_logger.info(f'locate_max = {t.locate_max()}')
    AVLTree_logger.info(f'locate_lower({l[len(l)//2]}) = {t.locate_lower(t.locate(l[len(l)//2]))}')
    AVLTree_logger.info(f'locate_higher({l[len(l)//2]}) = {t.locate_higher(t.locate(l[len(l)//2]))}')

    for n in l:
        t.remove(n, auto_rebalance=True)
    t.debugShow(label='remove_final')

def TESTAVL_insert_then_removeA():
    _AVL_insert_then_remove([x for x in range(10)], sys._getframe().f_code.co_name)

def TESTAVL_insert_then_removeB():
    _AVL_insert_then_remove([9,8,7,6,5,4,3,2,1], sys._getframe().f_code.co_name)

def TESTAVL_insert_then_removeC():
    _AVL_insert_then_remove([4, 6, 3, 1, 7, 9, 8, 5, 2], sys._getframe().f_code.co_name)


def TESTAVL_batch_insert_remove():
    if not os.path.exists(DBG_VIEW_ROOT):
        os.makedirs(DBG_VIEW_ROOT, exist_ok=True)
    t = AVLTree(name=sys._getframe().f_code.co_name, debug_level=2)

    total_data_size = 30
    batch_nb = 4

    value_list = [x for x in range(total_data_size)]
    shuffle(value_list)
    AVLTree_logger.info(f'{sys._getframe().f_code.co_name} batch_nb={batch_nb} value_list={value_list}')

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

    AVLTree_logger.info(f'insert_lists={insert_lists}')
    AVLTree_logger.info(f'remove_lists={remove_lists}')

    AVLTree_logger.info(t)
    for n in range(len(insert_lists)):

        list = insert_lists[n]
        AVLTree_logger.info(f"insert list={list}")

        for i in list:
            new_node = AVLTNode(i, host_tree=t)
            t.insert(new_node)
            AVLTree_logger.info(t.inorder_list_inc())
            AVLTree_logger.info(t.inorder_list_dec())

        del_list = remove_lists[n]

        AVLTree_logger.info(f"del_list={del_list}")
        for i in del_list:
            t.remove(i)
            AVLTree_logger.info(t.inorder_list_inc())
            AVLTree_logger.info(t.inorder_list_dec())


    del_list = remove_lists[-1]

    AVLTree_logger.info(f"del_list={del_list}")
    for i in del_list:
        t.remove(i)
        AVLTree_logger.info(t.inorder_list_inc())
        AVLTree_logger.info(t.inorder_list_dec())
    t.checkBalance()


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
    t = AVLTree(tree_name, debug_level=1)
    for n in l:
        new_node = AVLTNode(n, host_tree=t)
        t.insert(new_node, auto_rebalance=False)
    #TODO: 在所有插入完成后平衡，目前不成功
    # t._balance(t.locate_max(t.root), recurve_to_root=True)
    # # t._balance(t.root)
    # t._balance(t.locate_min(t.root), recurve_to_root=True)
    # t.debugShow(save_graph=True)



def TESTAVL_save_load():
    '''
    测试：导出/导入树
    '''
    l = [14987, 16059, 20287, 23639, 47623, 47624, 47625, 50672, 87188, 87189, 97471, 97472, 118563, 124604, 135780, 135781]
    random.seed(1000)
    shuffle(l)
    t = AVLTree('before_save', debug_level=2)
    for n in l:
        new_node = AVLTNode(n, host_tree=t)
        t.insert(new_node)
    saved = t.save()    #保存旧树结构
    print(saved)
    new_node = AVLTNode(50677, host_tree=t)
    t.insert(new_node)  #旧树新增一个节点 50677
    t.debugShow(label="save-final")

    tl = AVLTree('after_load', debug_level=2)      #新树装载旧树
    tl.load(saved)
    assert(t.size != tl.size)

    saved2 = tl.save()
    print(saved2)
    new_node = AVLTNode(60000, host_tree=tl)
    tl.insert(new_node) #新树新增一个节点 60000
    tl.debugShow(label="load-final")

    assert(t.size == tl.size)


def _RBT_insert_then_remove(l, s):
    if not os.path.exists(DBG_VIEW_ROOT):
        os.makedirs(DBG_VIEW_ROOT, exist_ok=True)

    t = RBTree(s, 1)
    for n in l:
        new_node = RBTNode(n, host_tree=t)
        t.insert(new_node, auto_rebalance=True)
    t.debugShow(label='insert_final')

    RBTree_logger.info(t.inorder_list_inc())
    RBTree_logger.info(t.inorder_list_dec())

    RBTree_logger.info(f'locate({l[len(l)//2]}) = {t.locate(l[len(l)//2])}')
    RBTree_logger.info(f'locate({max(l)+1}) = {t.locate(max(l)+1)}')
    RBTree_logger.info(f'locate({min(l)-1}) = {t.locate(min(l)-1)}')
    RBTree_logger.info(f'locate_min = {t.locate_min()}')
    RBTree_logger.info(f'locate_max = {t.locate_max()}')
    RBTree_logger.info(f'locate_lower({l[len(l)//2]}) = {t.locate_lower(t.locate(l[len(l)//2]))}')
    RBTree_logger.info(f'locate_higher({l[len(l)//2]}) = {t.locate_higher(t.locate(l[len(l)//2]))}')

    for n in l:
        t.remove(n, auto_rebalance=True)
    t.debugShow(label='remove_final')

def TESTRBT_insert_then_removeA():
    _RBT_insert_then_remove([x for x in range(10)], sys._getframe().f_code.co_name)

def TESTRBT_insert_then_removeB():
    _RBT_insert_then_remove([x for x in range(10,0,-1)], sys._getframe().f_code.co_name)

def TESTRBT_insert_then_removeC():
    _RBT_insert_then_remove([4, 6, 3, 1, 7, 9, 8, 5, 2], sys._getframe().f_code.co_name)



def TESTRBT_batch_insert_remove(seed, draw):
    if not os.path.exists(DBG_VIEW_ROOT):
        os.makedirs(DBG_VIEW_ROOT, exist_ok=True)
    random.seed(seed)
    if draw:
        debug_level = 2
    else:
        debug_level = 0
    t = RBTree(name=sys._getframe().f_code.co_name, debug_level=debug_level)

    total_data_size = 30
    batch_nb = 4

    value_list = [x for x in range(total_data_size)]
    shuffle(value_list)
    RBTree_logger.info(f'{sys._getframe().f_code.co_name} batch_nb={batch_nb} value_list={value_list}')

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

    RBTree_logger.info(f'insert_lists={insert_lists}')
    RBTree_logger.info(f'remove_lists={remove_lists}')

    RBTree_logger.info(t)
    for n in range(len(insert_lists)):

        list = insert_lists[n]
        RBTree_logger.info(f"insert list={list}")

        for i in list:
            new_node = RBTNode(i, host_tree=t)
            t.insert(new_node)
            RBTree_logger.info(t.inorder_list_inc())
            RBTree_logger.info(t.inorder_list_dec())

        del_list = remove_lists[n]

        RBTree_logger.info(f"del_list={del_list}")
        for i in del_list:
            t.remove(i)
            RBTree_logger.info(t.inorder_list_inc())
            RBTree_logger.info(t.inorder_list_dec())


    del_list = remove_lists[-1]

    RBTree_logger.info(f"del_list={del_list}")
    for i in del_list:
        t.remove(i)
        RBTree_logger.info(t.inorder_list_inc())
        RBTree_logger.info(t.inorder_list_dec())
    # t.checkBalance()
    assert t.size==0


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
    if tree_type=='AVL':
        ask = AVLTree(f'{tree_type}_ASK_')
        bid = AVLTree(f'{tree_type}_BID_')
    else:
        ask = RBTree(f'{tree_type}_ASK_')
        bid = RBTree(f'{tree_type}_BID_')
    with open(log_file, 'r') as f:
        while True:
            l = f.readline()
            if not l:break

            for cmd in [' remove ', ' insert ']:
                p = l.find(cmd)
                if p>=0:
                    v = int(l[p:].strip().split(' ')[1])
                    if l.find(' BID ')>0:
                        if cmd==' insert ':
                            if tree_type=='AVL':
                                new_node = AVLTNode(v, host_tree=bid)
                            else:
                                new_node = RBTNode(v, host_tree=bid)
                            bid.insert(new_node)
                        elif cmd==' remove ':
                            bid.remove(v)
                    elif l.find(' ASK ')>0:
                        if cmd==' insert ':
                            if tree_type=='AVL':
                                new_node = AVLTNode(v, host_tree=ask)
                            else:
                                new_node = RBTNode(v, host_tree=ask)
                            ask.insert(new_node)
                        elif cmd==' remove ':
                            ask.remove(v)

                    if bid_draw_size is not None and bid.size >= bid_draw_size:
                        bid.debugShow('max_size', force_draw=1)

                    if ask_draw_size is not None and ask.size >= ask_draw_size:
                        ask.debugShow('max_size', force_draw=1)

    if tree_type=='AVL':
        AVLTree_logger.info(f'ASK max size={ask.size_max}')
        AVLTree_logger.info(f'BID max size={bid.size_max}')
    else:
        RBTree_logger.info(f'ASK max size={ask.size_max}')
        RBTree_logger.info(f'BID max size={bid.size_max}')


