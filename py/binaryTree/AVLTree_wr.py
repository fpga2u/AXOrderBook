# -*- coding: utf-8 -*-
from __future__ import annotations
import uuid
from binaryTree.absTree import TNodeInRam, TreeWithRam
from binaryTree.util import *


import logging
AVLTree_logger = logging.getLogger(__name__)


##########
# AVL二叉树的节点
class AVLTNode(TNodeInRam):
    __slots__ = [
        'parent_addr',  #指向父节点，本节点是root端点时为None
        'is_left',      #本节点是左节点还是右节点，本节点是root端点时为None
        'value',        #本节点权重值
        'left_addr',    #指向左子节点 ram地址
        'right_addr',   #    右
        'left_height',  #左子节点高度，无左子节点时为0
        'right_height', #右
        'addr',
    ]
    def __init__(self, value=None, parent_addr:None|int=None, is_left=None, left_addr:None|int=None, right_addr:None|int=None):
        super(AVLTNode, self).__init__(value, parent_addr, is_left, left_addr, right_addr)
        self.left_height = 0
        self.right_height = 0

        # self.host_tree = host_tree
    
    @property
    def balance_factor(self):
        '''
        平衡系数，若=0，则左右子树完全平衡；若>0，则右子树高；若<0，则左子树高。
        '''
        return self.right_height - self.left_height

    @property
    def is_balance(self):
        return self.balance_factor>=-1 and self.balance_factor<=1
    
    def __str__(self):
        return f'{self.value} @{self.addr}'#f'AVLTNode({self.value} @{self.addr})'

    def save(self):
        '''
        存储节点信息
        '''
        data = {}
        for item in self.__slots__:
            attr = getattr(self, item)
            if isinstance(attr, AVLTNode):
                data[item] = attr.value
            elif attr is None:
                data[item] = None
            else:
                data[item] = attr
        return data

    def load(self, data):
        '''
        导入已存储的节点信息
        '''
        for attr in self.__slots__:
            value = data[attr]
            setattr(self, attr, value)



# AVL二叉树对象
class AVLTree(TreeWithRam):
    __slots__ = [
        'root_addr',
        'size',
        'size_max',
        'stk',
        'empty_head',
        'empty_tail',
        'graphSeq',
        'ram_access_stats',
        'value_list',
        'tree_name',
        'debug_level',

        'ram',
        'graph_last',

        'logger',
        'DBG',
        'INFO',
        'WARN',
        'ERR',
    ]
    def __init__(self, name='AVLTree', ram_depth=512, debug_level=0):
        '''
        debug_level:0=no-debug; 1=draw_tree; 2+=draw_tree_all
        '''
        super(AVLTree, self).__init__(name=name, ram_depth=ram_depth, debug_level=debug_level, node_impl=AVLTNode)

        ## 日志
        self.logger = logging.getLogger(f'{self.tree_name}')
        g_logger = logging.getLogger('main')
        self.logger.setLevel(g_logger.getEffectiveLevel())
        AVLTree_logger.setLevel(g_logger.getEffectiveLevel())
        for h in g_logger.handlers:
            self.logger.addHandler(h)
            AVLTree_logger.addHandler(h) #这里补上模块日志的handler

        self.DBG = self.logger.debug
        self.INFO = self.logger.info
        self.WARN = self.logger.warning
        self.ERR = self.logger.error

    def __str__(self):
        return f'AVLTree({self.tree_name})'

    def _drawNode_nest(self, graph, node:AVLTNode, node_tag, depth):
            '''
            绘制以某个节点为根节点的二叉树
            '''
            if depth>30:
                error='depth ovf!'
                self.ERR(error)
                raise error

            if node.left_addr is None and node.right_addr is None:
                return
            # 节点颜色
            if node.left_addr is not None:
                left_child = self.ram.at(node.left_addr)
                left_tag = str(uuid.uuid1())
                color = COLORS[left_child.value  % len(COLORS)]    #颜色与权重绑定，保持在颜色在树平衡前后的稳定性
                graph.node(left_tag, str(left_child.value), style='filled', fillcolor=color, color='black')    # 左节点
                graph.edge(node_tag, left_tag, label='L' + str(node.left_height))   # 左节点与其父节点的连线
                self._drawNode_nest(graph, left_child, left_tag, depth+1)
            else:
                left_tag = str(uuid.uuid1())
                graph.node(left_tag, '', style='filled', fillcolor='white', color='white')    # 左节点
                graph.edge(node_tag, left_tag, label='', fillcolor='white', color='white')   # 左节点与其父节点的连线

            if node.right_addr is not None:
                right_child = self.ram.at(node.right_addr)
                right_tag = str(uuid.uuid1())
                color = COLORS[right_child.value  % len(COLORS)]
                graph.node(right_tag, str(right_child.value), style='filled', fillcolor=color, color='black')
                graph.edge(node_tag, right_tag, label='R' + str(node.right_height))
                self._drawNode_nest(graph, right_child, right_tag, depth+1)
            else:
                right_tag = str(uuid.uuid1())
                graph.node(right_tag, '', style='filled', fillcolor='white', color='white')
                graph.edge(node_tag, right_tag, label='', fillcolor='white', color='white')


    #检查树 链接关系 和 平衡性 #for debug only
    def _checkLink(self):
        def check(addr:int):
            # self.DBG(node.value)
            node = self.ram.at(addr)
            if node.is_left is None:
                assert addr==self.root_addr
                assert node.parent_addr is None
            else:
                assert node.parent_addr is not None
                if node.is_left:
                    assert self.ram.at(node.parent_addr).left_addr==node.addr
                    assert node.value < self.ram.at(node.parent_addr).value
                    assert self.ram.at(node.parent_addr).left_height == max(node.left_height, node.right_height) + 1
                else:
                    assert self.ram.at(node.parent_addr).right_addr==node.addr
                    assert node.value > self.ram.at(node.parent_addr).value
                    assert self.ram.at(node.parent_addr).right_height == max(node.left_height, node.right_height) + 1
        self._preorder_nonrec(self.root_addr, check)

    def _checkBalance(self):
        '''
        检查平衡性
        '''
        pass

    #新增端点
    def _insert_helper(self, new_node:AVLTNode, auto_rebalance=True):
        """
        """
        assert new_node.value not in self.value_list or self.value_list[new_node.value]=='r', f'{self.tree_name} node:{new_node.value} exists!'
        self.value_list[new_node.value] = 'i'
        self.size += 1
        self.size_max = max(self.size, self.size_max)
        
        label = "insert " + str(new_node.value)

        #分配地址
        new_node.addr = self.empty_head
        self.empty_head = self.ram.read(self.empty_head).right_addr
        assert self.empty_tail is not None, f'{self.tree_name} ram address run out!' #必须总有一个是空的，不完全用尽

        if self.root_addr is None:
            self.ram.write(new_node)
            self.root_addr = new_node.addr

            self.debugShow(label)
            return

        # self.stk = simpleStack() #缓存所有的父节点地址，用于平衡
        current_node = self.ram.read(self.root_addr)
        ## insert under <current_node>
        while True:
            if current_node is None or new_node.value > current_node.value:
                if current_node.right_addr is None:
                    new_node.is_left = False
                    new_node.parent_addr = current_node.addr
                    current_node.right_addr = new_node.addr
                    # self.ram.write(new_node)
                    # self.ram.write(current_node)
                    break
                else:
                    self.stk.push(current_node.addr)
                    current_node = self.ram.read(current_node.right_addr)
            elif new_node.value < current_node.value:
                if current_node.left_addr is None:
                    new_node.is_left = True
                    new_node.parent_addr = current_node.addr
                    current_node.left_addr = new_node.addr
                    # self.ram.write(new_node)
                    # self.ram.write(current_node)
                    break
                else:                    
                    self.stk.push(current_node.addr)
                    current_node = self.ram.read(current_node.left_addr)
            else:
                # The level already exists
                break
        self.ram.write(new_node)
        self.ram.write(current_node)

        # udpate height
        while True:
            if new_node.is_left is None:
                break
            else:
                parent = self.ram.read(new_node.parent_addr)
                if new_node.is_left:
                    parent.left_height += 1
                    self.ram.write(parent)
                    if parent.left_height <= parent.right_height:
                        break
                else:
                    parent.right_height += 1
                    self.ram.write(parent)
                    if parent.right_height <= parent.left_height:
                        break
            new_node = parent

        self.debugShow(label)

        if auto_rebalance:
            ## balance: parent of <current_node>
            while not self.stk.is_empty():
                addr = self.stk.pop()
                parent = self.ram.read(addr)
                self._balance(parent)

    def _remove_node_helper(self, node:AVLTNode, auto_rebalance=True):
        if node is None:
            return
        label = f'remove_node {node.value}'
        self.size -= 1

        new_tail_addr = node.addr

        if node.left_addr is not None and node.right_addr is not None:
            node_right_child = self.ram.read(node.right_addr)
            node_left_child = self.ram.read(node.left_addr)
            min_node = self.locate_min(node_right_child)
            
            # Swap min_node and current node
            node_left_child.parent_addr = min_node.addr
            self.ram.write(node_left_child)
            if min_node.left_addr is not None:
                min_node_left_child = self.ram.read(min_node.left_addr)
                min_node_left_child.parent_addr = node.addr
                self.ram.write(min_node_left_child)
            node.left_addr, min_node.left_addr = min_node.left_addr, node.left_addr

            if min_node.addr != node_right_child.addr:
                node_right_child.parent_addr = min_node.addr
                self.ram.write(node_right_child)
                if min_node.right_addr is not None:
                    min_node_right_child = self.ram.read(min_node.right_addr)
                    min_node_right_child.parent_addr = node.addr
                    self.ram.write(min_node_right_child)
                node.right_addr, min_node.right_addr = min_node.right_addr, node.right_addr

                new_parent = self.ram.read(min_node.parent_addr)
                if node.is_left is None:
                    self.root_addr = min_node.addr
                else:
                    node_parent = self.ram.read(node.parent_addr)
                    if node.is_left:
                        node_parent.left_addr = min_node.addr
                    else:
                        node_parent.right_addr = min_node.addr
                    self.ram.write(node_parent)
                min_node.parent_addr = node.parent_addr

                if min_node.is_left:
                    new_parent.left_addr = node.addr
                else:
                    new_parent.right_addr = node.addr
                self.ram.write(new_parent)
                node.parent_addr = new_parent.addr
            else: #TODO: 合并到上面？
                # Swap node_right_child and node
                if min_node.right_addr is not None:
                    min_node_right_child = self.ram.read(min_node.right_addr)
                    min_node_right_child.parent_addr = node.addr
                    self.ram.write(min_node_right_child)
                node.right_addr, min_node.right_addr = min_node.right_addr, node.addr

                if node.is_left is None:
                    self.root_addr = min_node.addr
                else:
                    node_parent = self.ram.read(node.parent_addr)
                    if node.is_left:
                        node_parent.left_addr = min_node.addr
                    else:
                        node_parent.right_addr = min_node.addr
                    self.ram.write(node_parent)
                min_node.parent_addr, node.parent_addr = node.parent_addr, min_node.addr

            node.is_left, min_node.is_left = min_node.is_left, node.is_left
            node.left_height, min_node.left_height = min_node.left_height, node.left_height
            node.right_height, min_node.right_height = min_node.right_height, node.right_height

            self.ram.write(node)
            self.ram.write(min_node)

            self.debugShow(label + "_pre", check=False)
            
        if node.left_addr is not None:
            # Only left child
            if node.parent_addr is None: #del root
                self.root_addr = node.left_addr
                left_child = self.ram.read(node.left_addr)
                left_child.parent_addr = None
                left_child.is_left = None
                self.ram.write(left_child)
            else:
                node_parent = self.ram.read(node.parent_addr)
                left_child = self.ram.read(node.left_addr)
                if node.is_left:
                    node_parent.left_addr = node.left_addr
                    left_child.parent_addr = node_parent.addr
                else:
                    node_parent.right_addr = node.left_addr
                    left_child.parent_addr = node_parent.addr
                    left_child.is_left = False
                self.ram.write(node_parent)
                self.ram.write(left_child)
        elif node.right_addr is not None:
            # Only right child
            if node.parent_addr is None: #del root
                self.root_addr = node.right_addr
                right_child = self.ram.read(node.right_addr)
                right_child.parent_addr = None
                right_child.is_left = None
                self.ram.write(right_child)
            else:
                node_parent = self.ram.read(node.parent_addr)
                right_child = self.ram.read(node.right_addr)
                if node.is_left:
                    node_parent.left_addr = node.right_addr
                    right_child.parent_addr = node_parent.addr
                    right_child.is_left = True
                else:
                    node_parent.right_addr = node.right_addr
                    right_child.parent_addr = node_parent.addr
                self.ram.write(node_parent)
                self.ram.write(right_child)
        else:
            # No children
            if node.parent_addr is None: #del root
                self.root_addr = None
                self.graph_last = None
            else:
                node_parent = self.ram.read(node.parent_addr)
                if node.is_left:
                    node_parent.left_addr = None
                else:
                    node_parent.right_addr = None
                self.ram.write(node_parent)

        self.debugShow(label+' bef balance', check=False)
        
        tail = self.ram.read(self.empty_tail)
        tail.right_addr = new_tail_addr
        tail.addr = self.empty_tail
        self.ram.write(tail)
        self.empty_tail = new_tail_addr
        tail = self.ram.read(new_tail_addr)
        tail.right_addr = None
        self.ram.write(tail)

        if node.parent_addr is not None:
            node_parent = self.ram.read(node.parent_addr)
            latch_parent_addr = node_parent.addr

            # udpate height
            while True:
                if node.is_left is None:
                    break
                elif node.is_left:
                    node_parent.left_height -= 1
                    self.ram.write(node_parent)
                    if node_parent.left_height < node_parent.right_height:
                        break
                else:
                    node_parent.right_height -= 1
                    self.ram.write(node_parent)
                    if node_parent.right_height < node_parent.left_height:
                        break
                node = node_parent
                if node.parent_addr is None:
                    break
                node_parent = self.ram.read(node.parent_addr)
            

            if auto_rebalance:
                latch_parent = self.ram.read(latch_parent_addr)
                self._balance(latch_parent)
                if latch_parent is not None and latch_parent.parent_addr is not None:
                    self._balance(self.ram.read(latch_parent.parent_addr))

        self.debugShow(label)

    #平衡端点，在插入或删除端点后，要递归平衡其父节点
    #node is the point to hook nodes
    def _balance(self, node_param:AVLTNode, recurve_to_root=False):
        node = node_param

        #</<=; <=/> BID
        #<=/>=;<=/>=
        #</>=;</>=
        #<=/>=;</>= ASK
        while node is not None:
            balance_factor = node.right_height - node.left_height
            if balance_factor > 1:
                # right is heavier
                right_child = self.ram.read(node.right_addr)
                if right_child.balance_factor < 0: #TODO: < 和 <= 将导致树轻微单向倾斜，最终导致更适合BID或ASK
                    # right_child.left is heavier, RL case
                    self._rl_case(node, right_child)
                elif right_child.balance_factor >= 0:
                    # right_child.right is heavier, RR case
                    self._rr_case(node)
            elif balance_factor < -1:
                # left is heavier
                left_child = self.ram.read(node.left_addr)
                if left_child.balance_factor <= 0: #TODO: < 和 <= 将导致树轻微单向倾斜，最终导致更适合BID或ASK
                    # left_child.left is heavier, LL case
                    self._ll_case(node)
                elif left_child.balance_factor >= 0:
                    # left_child.right is heavier, LR case
                    self._lr_case(node, left_child)
            elif not recurve_to_root:
                # Everything's fine.
                break
            node = self.ram.read(node.parent_addr)


    # 挂载新端点
    def _hook_new_node(self, is_left:bool, new_hook:AVLTNode, parent:AVLTNode):
        if is_left is None:
            # node = self.root
            self.root_addr = new_hook.addr
            new_hook.parent_addr = None
            new_hook.is_left = None
        elif is_left:
            parent.left_addr = new_hook.addr
            new_hook.parent_addr = parent.addr
            new_hook.is_left = True
            self.ram.write(parent)
        else:
            parent.right_addr = new_hook.addr
            new_hook.parent_addr = parent.addr
            new_hook.is_left = False
            self.ram.write(parent)

        self.ram.write(new_hook)

        #更新父节点左右高度值
        #TODO: more efficient，提前终止？
        while True:
            if new_hook.parent_addr is None:
                break
            parent = self.ram.read(new_hook.parent_addr)
            new_height = max(new_hook.left_height, new_hook.right_height) + 1
            is_left = new_hook.is_left
            if is_left:
                if new_height==parent.left_height:
                    break
                self.DBG(f'{parent.value}.left_height: {parent.left_height}->{new_height}')
                parent.left_height = new_height
            else:
                if new_height==parent.right_height:
                    break
                self.DBG(f'{parent.value}.right_height: {parent.right_height}->{new_height}')
                parent.right_height = new_height
            self.ram.write(parent)
            new_hook = parent


    def _ll_case(self, child:AVLTNode):
        """Rotate Nodes for LL Case.

        Reference:
            https://en.wikipedia.org/wiki/File:Tree_Rebalancing.gif
        :return:
        """
        if child.parent_addr is not None:
            parent = self.ram.read(child.parent_addr)
        else:
            parent = None
        is_left = child.is_left

        label = f'LL {child.value} is_left({is_left})'

        new_hook = self.ram.read(child.left_addr)

        child.left_addr = new_hook.right_addr
        child.left_height = new_hook.right_height
        if new_hook.right_addr is not None:
            right_child = self.ram.read(new_hook.right_addr)
            right_child.parent_addr = child.addr
            right_child.is_left = True
            self.ram.write(right_child)

        new_hook.right_addr = child.addr
        new_hook.right_height = max(child.right_height, child.left_height) + 1
        child.parent_addr = new_hook.addr
        child.is_left = False
        self.ram.write(new_hook)
        self.ram.write(child)

        self._hook_new_node(is_left, new_hook, parent)

        self.debugShow(label)

    def _rr_case(self, node_param:AVLTNode):
        """Rotate Nodes for RR Case.

        Reference:
            https://en.wikipedia.org/wiki/File:Tree_Rebalancing.gif
        :return:
        """
        if node_param.parent_addr is not None:
            parent = self.ram.read(node_param.parent_addr)
        else:
            parent = None
        is_left = node_param.is_left

        label = f'RR {node_param.value} is_left({is_left})'
        child = node_param
        new_hook = self.ram.read(node_param.right_addr)

        child.right_addr = new_hook.left_addr
        child.right_height = new_hook.left_height
        if new_hook.left_addr is not None:
            left_child = self.ram.read(new_hook.left_addr)
            left_child.parent_addr = child.addr
            left_child.is_left = False
            self.ram.write(left_child)

        new_hook.left_addr = child.addr
        new_hook.left_height = max(child.left_height, child.right_height) + 1
        child.parent_addr = new_hook.addr
        child.is_left = True
        self.ram.write(new_hook)
        self.ram.write(child)

        self._hook_new_node(is_left, new_hook, parent)

        self.debugShow(label)

    def _lr_case(self, node:AVLTNode, child:AVLTNode):
        """Rotate Nodes for LR Case.

        Reference:
            https://en.wikipedia.org/wiki/File:Tree_Rebalancing.gif
        :return:
        """
        label = f'LR {node.value}'

        # child = self.ram.read(node.left_addr)
        node.left_addr = child.right_addr
        left_child = self.ram.read(node.left_addr)
        left_child.parent_addr = node.addr
        left_child.is_left = True
        child.right_addr = left_child.left_addr
        child.right_height = left_child.left_height
        if child.right_height > 0:
            right_child = self.ram.read(child.right_addr)
            right_child.parent_addr = child.addr
            right_child.is_left = False
            self.ram.write(right_child)

        left_child.left_addr = child.addr
        left_child.left_height = max(child.left_height, child.right_height) + 1
        child.parent_addr = node.left_addr
        self.ram.write(child)

        node.left_height = max(left_child.left_height, left_child.right_height) + 1
        self.ram.write(left_child)

        # self.ram.write(node)
        self.debugShow(label, check=False) #node没有写回，所以check会失败

        self._ll_case(node)


    def _rl_case(self, node:AVLTNode, child:AVLTNode):
        """Rotate Nodes for RL Case.

        Reference:
            https://en.wikipedia.org/wiki/File:Tree_Rebalancing.gif
        :return:
        """
        label = f'RL {node.value}'

        # child = node.right_child
        node.right_addr = child.left_addr
        right_child = self.ram.read(node.right_addr)
        right_child.parent_addr = node.addr
        right_child.is_left = False
        child.left_addr = right_child.right_addr
        child.left_height = right_child.right_height
        if child.left_height > 0:
            left_child = self.ram.read(child.left_addr)
            left_child.parent_addr = child.addr
            left_child.is_left = True
            self.ram.write(left_child)

        right_child.right_addr = child.addr
        right_child.right_height = max(child.right_height, child.left_height) + 1
        child.parent_addr = node.right_addr
        self.ram.write(child)

        node.right_height = max(right_child.right_height, right_child.left_height) + 1
        self.ram.write(right_child)

        # self.ram.write(node)
        self.debugShow(label, check=False) #node没有写回，所以check会失败

        self._rr_case(node)

    def save(self):
        '''
        导出树数据
        '''
        data = {}
        for item in self.__slots__:
            if item in ['logger', 'DBG', 'INFO', 'WARN', 'ERR', 'stk']:
                continue

            if item=='ram':
                r = {}
                for d in range(self.ram.depth):
                    v = self.ram.at(d)
                    if v is not None:
                        r[d] = v.save()
                data['ram'] = r
            elif item in ['graph_last']:
                data[item] = None
            else:
                attr = getattr(self, item)
                data[item] = attr

        return data

    def load(self, data):
        '''
        导入树数据
        '''
        for attr in self.__slots__:
            if attr in ['logger', 'DBG', 'INFO', 'WARN', 'ERR', 'ram', 'stk']:
                continue
            
            setattr(self, attr, data[attr])

        ## 日志
        self.logger = logging.getLogger(f'{self.tree_name}')
        g_logger = logging.getLogger('main')
        self.logger.setLevel(g_logger.getEffectiveLevel())
        for h in g_logger.handlers:
            self.logger.addHandler(h)
            AVLTree_logger.addHandler(h) #

        self.DBG = self.logger.debug
        self.INFO = self.logger.info
        self.WARN = self.logger.warning
        self.ERR = self.logger.error

        r = data['ram']
        self.ram.init(AVLTNode)
        for addr, n in r.items():
            new_node = AVLTNode()
            new_node.load(n)
            self.ram.data[int(addr)] = new_node


