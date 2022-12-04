# -*- coding: utf-8 -*-

from binaryTree.AVLTree import *
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