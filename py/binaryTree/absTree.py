# -*- coding: utf-8 -*-
from __future__ import annotations
from graphviz import Digraph
import abc
from copy import deepcopy
import uuid
import pandas as pd

pd.set_option('display.max_rows',100)
pd.set_option('display.width', 5000)
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.max_columns',None)

from functools import wraps

from tool.simpleStack import simpleStack
from binaryTree.util import *

## 树的抽象基类

class TNodeInRam(metaclass=abc.ABCMeta):
    '''存储在RAM中的树节点，仅保存父节点和左右子节点的地址'''
    def __init__(self, value=None, parent_addr:None|int=None, is_left=None, left_addr:None|int=None, right_addr:None|int=None):
        self.value = value  #节点在二叉树中的权重
        self.parent_addr = parent_addr
        self.is_left = is_left
        self.left_addr = left_addr
        self.right_addr = right_addr
        self.addr = None #在分配ram地址时赋值，在FPGA中并不存储在RAM中，而是读取时赋值

    @property
    def is_root(self):
        if self.parent_addr is None:
            assert self.is_left is None, "root with is_left not None"
        else:
            assert self.is_left is not None, "none-root with is_left is None"
        return self.parent_addr is None
    
    def __str__(self):
        return f'TNodeInRam({self.value} @{self.addr})'

    def __eq__(self, __o:TNodeInRam) -> bool:
        return self.addr == __o.addr

    @abc.abstractmethod
    def save(self):
        pass

    @abc.abstractmethod
    def load(self, data):
        pass

class NODE_BRAM():
    def __init__(self, depth:int, ram_name, node_impl=TNodeInRam):
        self.depth = depth
        self.ram_name = ram_name
        self.read_num = 0
        self.write_num = 0
        self.data:list[node_impl] = []
        self.init(node_impl)

    def read(self, addr:int)->TNodeInRam:
        self.read_num += 1
        return deepcopy(self.data[addr]) #读之后与ram中存储的数据再无关联

    def write(self, node:TNodeInRam):
        assert node.addr<self.depth, f'{self.ram_name} write addr={node.addr} / {self.depth} OVF!'
        self.write_num += 1
        self.data[node.addr] = node

    def at(self, addr)->TNodeInRam:
        '''无读写记录，用于debug'''
        assert addr<self.depth, f'{self.ram_name} read addr={addr} / {self.depth} OVF!'
        return self.data[addr]

    def init(self, node_impl):
        '''
        初始化成链表，right_addr指向下一个空地址
        '''
        self.data = []
        for i in range(self.depth):
            if i!=self.depth-1:
                node = node_impl(value=None, right_addr=i+1)
            else:
                node = node_impl()
            self.data.append(node)



## 统计ram读写次数
def profileit(f):
    @wraps(f)
    def wrap(*args, **kw):
        tree:TreeWithRam=args[0]
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
class TreeWithRam(metaclass=abc.ABCMeta):
    def __init__(self, name='TreeWithRam', ram_depth=512, debug_level=0, node_impl=TNodeInRam):
        '''
        debug_level:0=no-debug; 1=draw_tree; 2+=draw_tree_all
        '''
        self.root_addr = None
        self.size = 0   #leaf num
        self.size_max = 0
        self.ram = NODE_BRAM(ram_depth, ram_name=name+'_BRAM', node_impl=node_impl)
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
        
        ## 日志
        self.DBG = print
        self.INFO = print
        self.WARN = print
        self.ERR = print

    def __str__(self):
        return f'TreeWithRam({self.tree_name})'

    @property
    def ram_access_nb(self):
        '''
        return: (read_num, write_num, stk_push)
        '''
        return self.ram.read_num, self.ram.write_num, self.stk.push_nb

    def _drawTree(self, drawNode_nest)->Digraph:
        '''
        利用Graphviz实现二叉树的可视化
        '''
        # colors for labels of nodes
        graph = Digraph(comment='AVL Binary Tree')

        # 如果树非空
        if self.root_addr is not None:
            root = self.ram.at(self.root_addr)
            root_tag = str(uuid.uuid1())                # 根节点标签
            color = COLORS[root.value  % len(COLORS)]
            graph.node(root_tag, str(root), style='filled', fillcolor=color, color='black')     # 创建根节点
            drawNode_nest(graph, root, root_tag, 0)

        return graph

    def __print_helper(self, node:TNodeInRam, indent, last, s, depth, ret):
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
            ret.append(f'{s}{node}')
            s = ""
            if node.left_addr is not None:
                left_child = self.ram.at(node.left_addr)
                self.__print_helper(left_child, indent, False, s, depth+1, ret)
            if node.right_addr is not None:
                right_child = self.ram.at(node.right_addr)
                self.__print_helper(right_child, indent, True, s, depth+1, ret)

    def printTree(self):
        ret = []
        root = self.ram.at(self.root_addr)
        self.__print_helper(root, "", True, "", 0, ret)
        return '\n'.join(ret)

    @abc.abstractmethod
    def _drawNode_nest(self, graph, node, node_tag, depth):
        '''
        绘制以某个节点为根节点的二叉树，从node开始递归遍历所有子节点
        '''
        pass

    #打印树 #for debug only
    def debugShow(self, label="", check=True, force_draw=0):
        self.DBG(f"{label}")
        if self.root_addr is None:
            self.DBG(f" Tree is empty!")
            return
        if self.debug_level>0 or force_draw>0:
            graph = self._drawTree(self._drawNode_nest)
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
            except Exception as e:
                self.ERR(f"check {label} FAIL!")
                self.ERR('\n'+self.printTree())
                self.debugShow(f"check {label} FAIL", check=False, force_draw=1)
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

    def _preorder_nonrec(self, t:int, proc):
        '''
        先序遍历，仅用于debug
        '''
        s = simpleStack()
        while t is not None or not s.is_empty():
            while t is not None:        # 沿左分支下行
                proc(t)            # 先根序先处理根数据
                t = self.ram.at(t)
                s.push(t.right_addr)         # 右分支入栈
                t = t.left_addr
            t = s.pop()

    @abc.abstractmethod
    def _checkTree(self):
        '''
        检查连接关系
        '''
        pass

    def _checkRam(self, label):
        '''
        检查ram使用情况和空指针回收情况
        '''
        try:
            used_nb = self.size
            def count_sed(a):
                self.size -= 1
            self._preorder_nonrec(self.root_addr, count_sed)
            assert self.size==0
            self.size = used_nb

            addr = self.empty_head
            empty_nb = 0
            while addr is not None:
                empty_nb += 1
                addr = self.ram.at(addr).right_addr
            assert empty_nb+self.size==self.ram.depth
        except Exception as e:
            self.ERR(f"check {label} FAIL!")
            self.ERR('\n'+self.printTree())
            self.debugShow(f"check {label} FAIL", check=False, force_draw=1)
            raise e

    def getRoot(self)->TNodeInRam|None:
        if self.root_addr is None:
            return None
        return self.ram.read(self.root_addr)

    @profileit
    def dmy_writeback(self):
        '''模拟写回，仅增加统计计数'''
        self.ram.write_num += 1

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

    #新增端点
    @profileit
    def insert(self, new_node:TNodeInRam, auto_rebalance=True):
        # 检查外部操作正确性
        assert new_node.value not in self.value_list or self.value_list[new_node.value]=='r', f'{self.tree_name} node:{new_node.value} exists!'
        self.value_list[new_node.value] = 'i'
        self.size += 1
        self.size_max = max(self.size, self.size_max)

        #分配地址
        new_node.addr = self._get_head_before_insert()

        label = "insert " + str(new_node.value)
        self._insert_helper(new_node, auto_rebalance)

        # 最后检查ram
        self._checkRam(label)

    @abc.abstractmethod
    def _insert_helper(self, new_node:TNodeInRam, auto_rebalance=True):
        '''
        应用层配好new_node的数据和权重；
        node的addr已经在基类中被分配，本函数实现时不得再修改。
        '''
        pass

    @profileit
    def locate(self, value:int, root:TNodeInRam|None=None)->TNodeInRam|None:
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
    def locate_min(self, node:TNodeInRam|None = None)->TNodeInRam:
        if node is None:
            min_node = self.ram.read(self.root_addr)
        else:
            min_node = deepcopy(node)
        while min_node.left_addr is not None:
            min_node = self.ram.read(min_node.left_addr)
        return min_node

    @profileit
    def locate_max(self, node:TNodeInRam|None = None):
        if node is None:
            max_node = self.ram.read(self.root_addr)
        else:
            max_node = deepcopy(node)
        while max_node.right_addr is not None:
            max_node = self.ram.read(max_node.right_addr)
        return max_node

    # 找比某node更小的
    @profileit
    def locate_lower(self, node:TNodeInRam):
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
    def locate_higher(self, node:TNodeInRam):
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
        # 检查外部操作正确性
        if node is None:
            assert value not in self.value_list or self.value_list[value]=='r'
            self.DBG(f"{value} is not inserted or has already been removed.")
            return
        self.size -= 1

        self.remove_node(node, auto_rebalance)

        #用于检查外部操作，防止重复删除
        self.value_list[value] = 'r'

    def _get_head_before_insert(self):
        addr = self.empty_head
        self.empty_head = self.ram.read(self.empty_head).right_addr
        assert self.empty_head is not None, f'{self.tree_name} ram address run out!' #必须总有一个是空的，不完全用尽
        return addr

    def _update_tail_after_remove(self, new_tail_addr):
        assert self.empty_tail is not None, f'{self.tree_name} ram address run out!' #必须总有一个是空的，不完全用尽
        tail = self.ram.read(self.empty_tail)
        tail.right_addr = new_tail_addr
        tail.addr = self.empty_tail
        self.ram.write(tail)
        self.empty_tail = new_tail_addr
        tail = self.ram.read(new_tail_addr)
        tail.right_addr = None
        self.ram.write(tail)

    @profileit
    def remove_node(self, node:TNodeInRam, auto_rebalance=True):
        label = f'remove_node {node.value}'
        new_tail_addr = node.addr
        self._remove_node_helper(node, auto_rebalance)
        self._update_tail_after_remove(new_tail_addr)
        # 最后检查ram
        self._checkRam(label)

    @abc.abstractmethod
    def _remove_node_helper(self, node:TNodeInRam, auto_rebalance=True):
        '''
        node的ram地址将在基类中回收，本函数实现时无需处理。
        '''
        pass

    @abc.abstractmethod
    def save(self):
        '''
        导出树数据
        '''
        pass

    @abc.abstractmethod
    def load(self, data):
        '''
        导入树数据
        '''
        pass


