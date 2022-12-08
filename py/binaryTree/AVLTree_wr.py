# -*- coding: utf-8 -*-
from __future__ import annotations
from multiprocessing import parent_process
from turtle import left
from unicodedata import name
from graphviz import Digraph
import uuid
from tool.simpleStack import simpleStack
from binaryTree.util import *
from functools import wraps
import pandas as pd
from copy import deepcopy

pd.set_option('display.max_rows',100)
pd.set_option('display.width', 5000)
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.max_columns',None)

import logging
AVLTree_logger = logging.getLogger(__name__)


##########
# AVL二叉树的节点
class AVLTNode:
    __slots__ = [
        'parent_addr',  #指向父节点，本节点是root端点时为None
        'is_left',      #本节点是左节点还是右节点，本节点是root端点时为None
        'value',        #本节点权重值
        'left_addr',    #指向左子节点 ram地址
        'right_addr',   #    右
        'left_height',  #左子节点高度，无左子节点时为0
        'right_height', #右
        'addr',

        #for debug view
        # 'host_tree',     #指向本节点所属的二叉树
    ]
    def __init__(self, value=None, parent_addr:None|int=None, is_left=None, left_addr:None|int=None, right_addr:None|int=None):
        self.value = value  #节点在二叉树中的权重
        self.parent_addr = parent_addr
        self.is_left = is_left
        self.left_addr = left_addr
        self.right_addr = right_addr
        self.left_height = 0
        self.right_height = 0
        self.addr = None #在分配ram地址时赋值，在FPGA中并不存储在RAM中，而是读取时赋值

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

    @property
    def is_root(self):
        if self.parent_addr is None:
            assert self.is_left is None, "root with is_left not None"
        else:
            assert self.is_left is not None, "none-root with is_left is None"
        return self.parent_addr is None
    
    def __str__(self):
        return f'AVLTNode({self.value})'

    def __eq__(self, __o:AVLTNode) -> bool:
        return self.addr == __o.addr

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



class NODE_BRAM():
    def __init__(self, depth:int, ram_name='NODE_BRAM'):
        self.depth = depth
        self.ram_name = ram_name
        self.read_num = 0
        self.write_num = 0
        self.data:list[AVLTNode] = []
        self.init()

    def read(self, addr:int)->AVLTNode:
        self.read_num += 1
        return deepcopy(self.data[addr])

    def write(self, value:AVLTNode):
        assert value.addr<self.depth, f'{self.ram_name} write addr={value.addr} / {self.depth} OVF!'
        self.write_num += 1
        self.data[value.addr] = value

    def at(self, addr)->AVLTNode:
        '''无读写记录，用于debug'''
        assert addr<self.depth, f'{self.ram_name} read addr={addr} / {self.depth} OVF!'
        return self.data[addr]

    def init(self):
        '''
        初始化成链表，right_addr指向下一个空地址
        '''
        for i in range(self.depth):
            if i!=self.depth-1:
                node = AVLTNode(right_addr=i+1)
            else:
                node = AVLTNode()
            self.data.append(node)


## 统计ram读写次数
def profileit(f):
    @wraps(f)
    def wrap(*args, **kw):
        tree=args[0]
        _ram_access_nb = tree.ram_access_nb
        tree.stk.clr() #即使f内部没有用到stk，也清一次

        result = f(*args, **kw)

        rd_inc = tree.ram_access_nb[0]-_ram_access_nb[0]
        wr_inc = tree.ram_access_nb[1]-_ram_access_nb[1]
        stk_push = tree.ram_access_nb[2]*2 #读写总是成对
        tree.DBG(f'{f.__name__} {_ram_access_nb}->{tree.ram_access_nb} =+({rd_inc}, {wr_inc}, {stk_push})')

        if f.__name__ not in tree.ram_access_stats:
            tree.ram_access_stats[f.__name__] = {
                'rd':[rd_inc],
                'wr':[wr_inc],
                'stk':[stk_push],
            }
        else:
            tree.ram_access_stats[f.__name__]['rd'].append(rd_inc)
            tree.ram_access_stats[f.__name__]['wr'].append(wr_inc)
            tree.ram_access_stats[f.__name__]['stk'].append(stk_push)

        return result
    return wrap


# AVL二叉树对象
class AVLTree:
    def __init__(self, name='AVLTree', debug_level=0):
        '''
        debug_level:0=no-debug; 1=draw_tree; 2+=draw_tree_all
        '''
        self.root_addr = None
        self.size = 0   #leaf num
        self.size_max = 0
        self.ram = NODE_BRAM(512, ram_name=name+'_BRAM')
        self.stk = simpleStack()
        self.empty_head = 0
        self.empty_tail = self.ram.depth-1

        #for debug only
        self.graph_last = None
        self.graphSeq = 0

        self.ram_access_stats = {}

        #for debug check
        self.value_list = {}
        self.tree_name = name
        self.debug_level = debug_level
        self.graph_last = None
        
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
        return f'AVLTree({self.tree_name}) id:{id(self)}'

    @property
    def ram_access_nb(self):
        '''
        return: (read_num, write_num, stk_push)
        '''
        return self.ram.read_num, self.ram.write_num, self.stk.push_nb

    def _drawTree(self):
        '''
        利用Graphviz实现二叉树的可视化
        '''
        # colors for labels of nodes
        graph = Digraph(comment='AVL Binary Tree')

        def drawNode(node:AVLTNode, node_tag, depth):
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
                drawNode(left_child, left_tag, depth+1)
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
                drawNode(right_child, right_tag, depth+1)
            else:
                right_tag = str(uuid.uuid1())
                graph.node(right_tag, '', style='filled', fillcolor='white', color='white')
                graph.edge(node_tag, right_tag, label='', fillcolor='white', color='white')

        # 如果树非空
        if self.root_addr is not None:
            root = self.ram.at(self.root_addr)
            root_tag = str(uuid.uuid1())                # 根节点标签
            color = COLORS[root.value  % len(COLORS)]
            graph.node(root_tag, str(root.value), style='filled', fillcolor=color, color='black')     # 创建根节点
            drawNode(root, root_tag, 0)

        return graph

    def __print_helper(self, node:AVLTNode, indent, last, s, depth, print):
        if depth>30:
            error='depth ovf!'
            self.ERR(error)
            raise error

        if node is not None:
            s += indent
            if last:
                s += "R----  "
                indent += "     "
            else:
                s += "L----  "
                indent += "|    "
            print(f'{s}{str(node.value)}')
            s = ""
            if node.left_addr is not None:
                left_child = self.ram.at(node.left_addr)
                self.__print_helper(left_child, indent, False, s, depth+1, print)
            if node.right_addr is not None:
                right_child = self.ram.at(node.right_addr)
                self.__print_helper(right_child, indent, True, s, depth+1, print)

    def printTree(self, printer=None):
        if printer is None:
            printer = print
        root = self.ram.at(self.root_addr)
        self.__print_helper(root, "", True, "", 0, print=printer)

    #打印树 #for debug only
    def debugShow(self, label="", check=True, force_draw=0):
        self.DBG(f"{label}")
        if self.root_addr is None:
            self.DBG(f" Tree is empty!")
            return
        if self.debug_level>0 or force_draw>0:
            graph = self._drawTree()
            if self.debug_level>1 or force_draw>1:    #显示上一步和当前
                if self.graph_last is None:
                    self.graph_last = graph
                else:
                    new_step = graph
                    graph = self.graph_last
                    graph.subgraph(new_step)
                    self.graph_last = new_step
            save_path = f'{DBG_VIEW_ROOT}/{self.tree_name}_show{self.graphSeq:05d}_{label}'
            r = graph.render(format='png', filename=save_path)
            self.DBG(f' {r}')
        self.graphSeq+=1

        if check:
            try:
                self._checkTree()
                self._checkRam()
            except Exception as e:
                self.ERR(f"check {label} FAIL!")
                self.printTree(self.ERR)
                self.debugShow("checkTree FAIL", check=False, force_draw=1)
                raise e

    def _describe_ram_access_stats(self):
        m = []
        for cmd, s in self.ram_access_stats.items():
            df = pd.DataFrame(s)
            df.columns=[cmd+"."+x for x in s]
            df = df.loc[:, df.any()]
            m.append(df)
        m = pd.concat(m, axis=1)
        return f"{self.tree_name} ram access stats:\n"+str(m.describe()) + f"\n{self.tree_name} ram access sum:\n" + str(m.sum())

    def profile(self):
        return self._describe_ram_access_stats()

    def preorder_nonrec(self, t:int, proc):
        s = simpleStack()
        while t is not None or not s.is_empty():
            while t is not None:        # 沿左分支下行
                proc(t)            # 先根序先处理根数据
                t = self.ram.at(t)
                s.push(t.right_addr)         # 右分支入栈
                t = t.left_addr
            t = s.pop()

    #检查树 链接关系 和 平衡性 #for debug only
    def _checkTree(self):
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
        self.preorder_nonrec(self.root_addr, check)

    def _checkRam(self):
        used_nb = self.size
        def count_sed(a):
            self.size -= 1
        self.preorder_nonrec(self.root_addr, count_sed)
        assert self.size==0
        self.size = used_nb

        addr = self.empty_head
        empty_nb = 0
        while addr is not None:
            empty_nb += 1
            addr = self.ram.at(addr).right_addr
        assert empty_nb+self.size==self.ram.depth

    #验证树平衡性 #for debug only
    def checkBalance(self):
        def check(addr:int):
            node = self.ram.at(addr)
            assert node.left_height < node.right_height + 2
            assert node.right_height < node.left_height + 2
        self.preorder_nonrec(self.root_addr, check)

    def getRoot(self)->AVLTNode|None:
        if self.root_addr is None:
            return None
        return self.ram.read(self.root_addr)

    @profileit
    def dmy_writeback(self):
        '''模拟写回，仅增加统计计数'''
        self.ram.write_num += 1

    #新增端点
    @profileit
    def insert(self, new_node:AVLTNode, auto_rebalance=True):
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

    #中序非递归遍历，从小到大输出所有序列
    @profileit
    def inorder_list_inc(self):
        # self.stk = simpleStack()
        t = self.root_addr
        l = []
        while t is not None or not self.stk.is_empty():
            while t is not None:
                node = self.ram.read(t)
                self.stk.push(node)
                t = node.left_addr
            node = self.stk.pop()
            l.append(node.value)
            t = node.right_addr
        return l

    #中序非递归遍历，从大到小输出所有序列
    @profileit
    def inorder_list_dec(self):
        # self.stk = simpleStack()
        t = self.root_addr
        l = []
        while t is not None or not self.stk.is_empty():
            while t is not None:
                node = self.ram.read(t)
                self.stk.push(node)
                t = node.right_addr
            node = self.stk.pop()
            l.append(node.value)
            t = node.left_addr
        return l

    @profileit
    def locate(self, value:int, root:AVLTNode|None=None)->AVLTNode|None:
        if self.root_addr is None:
            return

        if root is None:
            node = self.ram.read(self.root_addr)
        else:
            node = root

        while True:
            if node.value < value:
                if node.right_addr is None:
                    return
                node = self.ram.read(node.right_addr)
            elif node.value > value:
                if node.left_addr is None:
                    return
                node = self.ram.read(node.left_addr)
            else:
                return node

    @profileit
    def locate_min(self, node:AVLTNode|None = None)->AVLTNode:
        if node is None:
            min_node = self.ram.read(self.root_addr)
        else:
            min_node = deepcopy(node)
        while min_node.left_addr is not None:
            min_node = self.ram.read(min_node.left_addr)
        return min_node

    @profileit
    def locate_max(self, node:AVLTNode|None = None):
        if node is None:
            max_node = self.ram.read(self.root_addr)
        else:
            max_node = deepcopy(node)
        while max_node.right_addr is not None:
            max_node = self.ram.read(max_node.right_addr)
        return max_node

    # 找比某node更小的
    @profileit
    def locate_lower(self, node:AVLTNode):
        if node.left_addr is not None:
            left_child = self.ram.read(node.left_addr)
            return self.locate_max(left_child)
        else:
            lower_addr = node.parent_addr
            lower = None
            while lower_addr is not None:
                lower = self.ram.read(lower_addr)
                if lower.value > node.value:
                    lower_addr = lower.parent_addr
                else:
                    break
            if lower is not None and lower.value < node.value:
                return lower
            return None

    @profileit
    def locate_higher(self, node:AVLTNode):
        if node.right_addr is not None:
            right_child = self.ram.read(node.right_addr)
            return self.locate_min(right_child)
        else:
            higher_addr = node.parent_addr
            higher = None
            while higher_addr is not None:
                higher = self.ram.read(higher_addr)
                if higher.value < node.value:
                    higher_addr = higher.parent_addr
                else:
                    break
            if higher is not None and higher.value > node.value:
                return higher
            return None

    def remove(self, value:int, auto_rebalance=True):

        node = self.locate(value)
        if node is None:
            assert value not in self.value_list or self.value_list[value]=='r'
            self.DBG(f"{value} is not inserted or has already been removed.")
            return
        self.remove_node(node, auto_rebalance)
        self.value_list[value] = 'r'

    @profileit
    def remove_node(self, node:AVLTNode, auto_rebalance=True):
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
                if right_child.balance_factor <= 0: #TODO: < 和 <= 将导致树轻微单向倾斜，最终导致更适合BID或ASK
                    # right_child.left is heavier, RL case
                    self._rl_case(node, right_child)
                elif right_child.balance_factor >= 0:
                    # right_child.right is heavier, RR case
                    self._rr_case(node)
            elif balance_factor < -1:
                # left is heavier
                left_child = self.ram.read(node.left_addr)
                if left_child.balance_factor < 0: #TODO: < 和 <= 将导致树轻微单向倾斜，最终导致更适合BID或ASK
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
        for d in range(self.ram.depth):
            v = self.ram.at(d)
            if v is not None:
                data[d] = v
        return {'ram' : data, 'size':self.size}

    def load(self, data):
        '''
        导入树数据
        '''
        self.size = data['size']
        data = data['ram']
        self.ram.init()
        for addr, n in data.items():
            new_node = AVLTNode()
            new_node.load(n)
            self.ram.data[addr] = new_node


