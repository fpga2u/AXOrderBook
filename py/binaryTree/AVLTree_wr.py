# -*- coding: utf-8 -*-
from __future__ import annotations
from multiprocessing import parent_process
from turtle import left
from graphviz import Digraph
import uuid
from tool.simpleStack import simpleStack
from binaryTree.util import *
from functools import wraps

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
    def is_root(self):
        if self.parent_addr is None:
            assert self.is_left is None, "root with is_left not None"
        else:
            assert self.is_left is not None, "none-root with is_left is None"
        return self.parent_addr is None
    
    def __str__(self):
        return f'AVLTNode({self.value})'

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
        return self.at(addr)

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


def profileit(f):
    @wraps(f)
    def wrap(*args, **kw):
        tree=args[0]
        _ram_access_nb = tree.ram_access_nb
        result = f(*args, **kw)
        tree.DBG(f'{f.__name__} {_ram_access_nb}->{tree.ram_access_nb} =+({tree.ram_access_nb[0]-_ram_access_nb[0]}, {tree.ram_access_nb[1]-_ram_access_nb[1]})')

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
        self.ram = NODE_BRAM(16*1024, ram_name=name+'_BRAM')
        self.empty_head = 0
        self.empty_tail = self.ram.depth-1

        #for debug only
        self.graph_last = None
        self.graphSeq = 0

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
        return: (read_num, write_num)
        '''
        return self.ram.read_num, self.ram.write_num

    def _drawTree(self):
        '''
        利用Graphviz实现二叉树的可视化
        '''
        # colors for labels of nodes
        graph = Digraph(comment='AVL Binary Tree')

        def drawNode(node:AVLTNode, node_tag):
            '''
            绘制以某个节点为根节点的二叉树
            '''
            if node.left_addr is None and node.right_addr is None:
                return
            # 节点颜色
            if node.left_addr is not None:
                left_child = self.ram.at(node.left_addr)
                left_tag = str(uuid.uuid1())
                color = COLORS[left_child.value  % len(COLORS)]    #颜色与权重绑定，保持在颜色在树平衡前后的稳定性
                graph.node(left_tag, str(left_child.value), style='filled', fillcolor=color, color='black')    # 左节点
                graph.edge(node_tag, left_tag, label='L' + str(node.left_height))   # 左节点与其父节点的连线
                drawNode(left_child, left_tag)
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
                drawNode(right_child, right_tag)
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
            drawNode(root, root_tag)

        return graph

    def __print_helper(self, node:AVLTNode, indent, last, s, print):
        if node != None:
            # sys.stdout.write(indent)
            s += indent
            if last:
                # sys.stdout.write("R----  ")
                s += "R----  "
                indent += "     "
            else:
                # sys.stdout.write("L----  ")
                s += "L----  "
                indent += "|    "
            # print(str(node))
            print(f'{s}{str(node.value)}')
            s = ""
            if node.left_addr is not None:
                left_child = self.ram.at(node.left_addr)
                self.__print_helper(left_child, indent, False, s, print)
            if node.right_addr is not None:
                right_child = self.ram.at(node.right_addr)
                self.__print_helper(right_child, indent, True, s, print)

    def printTree(self, printer=None):
        if printer is None:
            printer = print
        root = self.ram.at(self.root_addr)
        self.__print_helper(root, "", True, "", print=printer)

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
            self._checkTree()

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
                assert addr==0
                assert node.parent_addr is None
            else:
                assert node.parent_addr is not None
                if node.is_left:
                    assert id(self.ram.at(self.ram.at(node.parent_addr).left_addr))==id(node)
                    assert node.value < self.ram.at(node.parent_addr).value
                    assert self.ram.at(node.parent_addr).left_height == max(node.left_height, node.right_height) + 1
                else:
                    assert id(self.ram.at(self.ram.at(node.parent_addr).right_addr))==id(node)
                    assert node.value > self.ram.at(node.parent_addr).value
                    assert self.ram.at(node.parent_addr).right_height == max(node.left_height, node.right_height) + 1
        self.preorder_nonrec(0, check)

    #验证树平衡性 #for debug only
    def checkBalance(self):
        def check(addr:int):
            node = self.ram.at(addr)
            assert node.left_height < node.right_height + 2
            assert node.right_height < node.left_height + 2
        self.preorder_nonrec(0, check)

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

        if self.root_addr is None:
            self.ram.write(new_node)
            self.root_addr = new_node.addr

            self.debugShow(label)
            return

        stk = simpleStack() #缓存所有的父节点地址，用于平衡
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
                    stk.push(current_node)
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
                    stk.push(current_node)
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
            while True:
                parent = stk.pop()
                if parent is None:
                    break
                self._balance(parent)

    #中序非递归遍历，从小到大输出所有序列
    @profileit
    def inorder_list_inc(self):
        s = simpleStack()
        t = self.root_addr
        l = []
        while t is not None or not s.is_empty():
            while t is not None:
                node = self.ram.read(t)
                s.push(node)
                t = node.left_addr
            node = s.pop()
            l.append(node.value)
            t = node.right_addr
        return l

    #中序非递归遍历，从大到小输出所有序列
    @profileit
    def inorder_list_dec(self):
        s = simpleStack()
        t = self.root_addr
        l = []
        while t is not None or not s.is_empty():
            while t is not None:
                node = self.ram.read(t)
                s.push(node)
                t = node.right_addr
            node = s.pop()
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
            min_node = node
        while min_node.left_addr is not None:
            min_node = self.ram.read(min_node.left_addr)
        return min_node

    @profileit
    def locate_max(self, node:AVLTNode|None = None):
        if node is None:
            max_node = self.ram.read(self.root_addr)
        else:
            max_node = node
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
            while higher_addr is not None:
                higher = self.ram.read(higher_addr)
                if higher.value < node.value:
                    higher_addr = higher.parent_addr
                else:
                    break
            if higher is not None and higher.value > node.value:
                return higher
            return None

    @profileit
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
        if node.left_child and node.right_child:
            min_node = self.locate_min(node.right_child)
            
            # Swap min_node and current node
            node.left_child.parent = min_node
            if min_node.left_child:
                min_node.left_child.parent = node
            node.left_child, min_node.left_child = min_node.left_child, node.left_child

            node.right_child.parent = min_node
            if min_node.right_child:
                min_node.right_child.parent = node
            node.right_child, min_node.right_child = min_node.right_child, node.right_child

            new_parent = min_node.parent
            if node.is_left is None:
                self.root = min_node
            elif node.is_left:
                node.parent.left_child = min_node
            else:
                node.parent.right_child = min_node
            min_node.parent = node.parent

            if min_node.is_left:
                new_parent.left_child = node
            else:
                new_parent.right_child = node
            node.parent = new_parent
            
            # node.parent, min_node.parent = min_node.parent, node.parent
            node.is_left, min_node.is_left = min_node.is_left, node.is_left
            node.left_height, min_node.left_height = min_node.left_height, node.left_height
            node.right_height, min_node.right_height = min_node.right_height, node.right_height

            self.debugShow(label + "_pre", check=False)
            
        if node.left_child:
            # Only left child
            if not node.parent: #del root
                self.root = node.left_child
                node.left_child.parent = None
                node.left_child.is_left = None
            else:
                if node.is_left:
                    node.parent.left_child = node.left_child
                    node.left_child.parent = node.parent
                else:
                    node.parent.right_child = node.left_child
                    node.left_child.parent = node.parent
                    node.left_child.is_left = False
        elif node.right_child:
            # Only right child
            if not node.parent: #del root
                self.root = node.right_child
                node.right_child.parent = None
                node.right_child.is_left = None
            else:
                if node.is_left:
                    node.parent.left_child = node.right_child
                    node.right_child.parent = node.parent
                    node.right_child.is_left = True
                else:
                    node.parent.right_child = node.right_child
                    node.right_child.parent = node.parent
        else:
            # No children
            if not node.parent: #del root
                self.root = None
                self.graph_last = None
            else:
                if node.is_left:
                    node.parent.left_child = None
                else:
                    node.parent.right_child = None

        latch_parent = node.parent

        # udpate height
        while True:
            if node.is_left is None:
                break
            elif node.is_left:
                node.parent.left_height -= 1
                if node.parent.left_height < node.parent.right_height:
                    break
            else:
                node.parent.right_height -= 1
                if node.parent.right_height < node.parent.left_height:
                    break
            node = node.parent
        
        self.debugShow(label)

        if auto_rebalance:
            self._balance(latch_parent)
            if latch_parent:
                self._balance(latch_parent.parent)

    #平衡端点，在插入或删除端点后，要递归平衡其父节点
    #node is the point to hook nodes
    @profileit
    def _balance(self, node_param:AVLTNode, recurve_to_root=False):
        node = node_param
        _ram_access_nb = self.ram_access_nb

        while node is not None:
            balance_factor = node.right_height - node.left_height
            if balance_factor > 1:
                # right is heavier
                right_child = self.ram.read(node.right_addr)
                if right_child.balance_factor < 0: #TODO: 用<=是更严格地balance
                    # right_child.left is heavier, RL case
                    self._rl_case(node, right_child)
                elif right_child.balance_factor >= 0:
                    # right_child.right is heavier, RR case
                    self._rr_case(node)
            elif balance_factor < -1:
                # left is heavier
                left_child = self.ram.read(node.left_addr)
                if left_child.balance_factor <= 0: #TODO: 用<=是更严格地balance
                    # left_child.left is heavier, LL case
                    self._ll_case(node)
                elif left_child.balance_factor > 0:
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

        node.left_height = max(left_child.left_height, left_child.right_height) + 1
        # self.ram.write(node)
        self.ram.write(left_child)

        self.debugShow(label)

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

        node.right_height = max(right_child.right_height, right_child.left_height) + 1
        # self.ram.write(node)
        self.ram.write(right_child)

        self.debugShow(label)

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


