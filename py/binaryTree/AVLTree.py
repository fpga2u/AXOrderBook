# -*- coding: utf-8 -*-
from __future__ import annotations
from graphviz import Digraph
import uuid
from tool.simpleStack import simpleStack
from binaryTree.util import *
import sys

import logging
AVLTree_logger = logging.getLogger(__name__)


##########
# AVL二叉树的节点
class AVLTNode:
    __slots__ = [
        'parent',       #指向父节点，本节点是root端点时为None
        'is_left',      #本节点是左节点还是右节点，本节点是root端点时为None
        'value',        #本节点权重值
        'left_child',   #指向左子节点
        'right_child',  #    右
        'left_height',  #左子节点高度，无左子节点时为0
        'right_height', #右

        #for debug view
    ]
    def __init__(self, value=None, parent:None|AVLTNode=None, is_left=None, left_child:None|AVLTNode=None, right_child:None|AVLTNode=None):
        self.value = value  #节点在二叉树中的权重
        self.parent = parent
        self.is_left = is_left
        self.left_child = left_child
        self.right_child = right_child
        self.left_height = 0
        self.right_height = 0

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
        if self.parent is None:
            assert self.is_left is None, "root with is_left not None"
        else:
            assert self.is_left is not None, "none-root with is_left is None"
        return self.parent is None
    
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


# AVL二叉树对象
class AVLTree:
    def __init__(self, name='AVLTree', debug_level=0):
        '''
        debug_level:0=no-debug; 1=draw_tree; 2+=draw_tree_all
        '''
        self.root = None
        self.size = 0   #leaf num
        self.size_max = 0

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
            if node.left_child is None and node.right_child is None:
                return
            # 节点颜色
            if node.left_child is not None:
                left_tag = str(uuid.uuid1())
                color = COLORS[node.left_child.value  % len(COLORS)]    #颜色与权重绑定，保持在颜色在树平衡前后的稳定性
                graph.node(left_tag, str(node.left_child.value), style='filled', fillcolor=color, color='black')    # 左节点
                graph.edge(node_tag, left_tag, label='L' + str(node.left_height))   # 左节点与其父节点的连线
                drawNode(node.left_child, left_tag)
            else:
                left_tag = str(uuid.uuid1())
                graph.node(left_tag, '', style='filled', fillcolor='white', color='white')    # 左节点
                graph.edge(node_tag, left_tag, label='', fillcolor='white', color='white')   # 左节点与其父节点的连线

            if node.right_child is not None:
                right_tag = str(uuid.uuid1())
                color = COLORS[node.right_child.value  % len(COLORS)]
                graph.node(right_tag, str(node.right_child.value), style='filled', fillcolor=color, color='black')
                graph.edge(node_tag, right_tag, label='R' + str(node.right_height))
                drawNode(node.right_child, right_tag)
            else:
                right_tag = str(uuid.uuid1())
                graph.node(right_tag, '', style='filled', fillcolor='white', color='white')
                graph.edge(node_tag, right_tag, label='', fillcolor='white', color='white')

        # 如果树非空
        if self.root is not None:
            root_tag = str(uuid.uuid1())                # 根节点标签
            color = COLORS[self.root.value  % len(COLORS)]
            graph.node(root_tag, str(self.root.value), style='filled', fillcolor=color, color='black')     # 创建根节点
            drawNode(self.root, root_tag)

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
            self.__print_helper(node.left_child, indent, False, s, depth+1, print)
            self.__print_helper(node.right_child, indent, True, s, depth+1, print)

    def printTree(self, printer=None):
        if printer is None:
            printer = print
        self.__print_helper(self.root, "", True, "", 0, print=printer)

    #打印树 #for debug only
    def debugShow(self, label="", check=True, force_draw=0):
        self.DBG(f"{label}")
        if not self.root:
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

    #检查树 链接关系 和 平衡性 #for debug only
    def _checkTree(self):
        def check(node:AVLTNode):
            # self.DBG(node.value)
            try:
                if node.is_left is None:
                    assert node.parent is None
                    assert id(node)==id(self.root)
                else:
                    assert node.parent is not None
                    if node.is_left:
                        assert id(node.parent.left_child)==id(node)
                        assert node.value < node.parent.value
                        assert node.parent.left_height == max(node.left_height, node.right_height) + 1
                    else:
                        assert id(node.parent.right_child)==id(node)
                        assert node.value > node.parent.value
                        assert node.parent.right_height == max(node.left_height, node.right_height) + 1
            except Exception as e:
                self.ERR(f"checkTree FAIL!")
                self.printTree(self.ERR)
                self.debugShow("checkTree FAIL", check=False, force_draw=1)
                raise e
        preorder_nonrec(self.root, check)

    def profile(self):
        return ""

    #验证树平衡性 #for debug only
    def checkBalance(self):
        def check(node:AVLTNode):
            assert node.left_height < node.right_height + 2
            assert node.right_height < node.left_height + 2
        preorder_nonrec(self.root, check)

    def getRoot(self)->AVLTNode|None:
        return self.root

    def dmy_writeback(self):
        pass

    #新增端点
    def insert(self, new_node:AVLTNode, auto_rebalance=True):
        """
        """
        assert new_node.value not in self.value_list or self.value_list[new_node.value]=='r', f'{self.tree_name} node:{new_node.value} exists!'
        self.value_list[new_node.value] = 'i'
        self.size += 1
        self.size_max = max(self.size, self.size_max)
        
        label = "insert " + str(new_node.value)
        if self.root is None:
            self.root = new_node
            self.debugShow(label)
            return
        stk = simpleStack() #缓存所有的父节点，用于平衡
        current_node = self.root
        ## insert under <current_node>
        while True:
            if current_node is None or new_node.value > current_node.value:
                if current_node.right_child is None:
                    new_node.is_left = False
                    new_node.parent = current_node
                    current_node.right_child = new_node
                    break
                else:
                    stk.push(current_node)
                    current_node = current_node.right_child
            elif new_node.value < current_node.value:
                if current_node.left_child is None:
                    new_node.is_left = True
                    new_node.parent = current_node
                    current_node.left_child = new_node
                    break
                else:                    
                    stk.push(current_node)
                    current_node = current_node.left_child
            else:
                # The level already exists
                break

        # udpate height
        while True:
            if new_node.is_left is None:
                break
            elif new_node.is_left:
                new_node.parent.left_height += 1
                if new_node.parent.left_height <= new_node.parent.right_height:
                    break
            else:
                new_node.parent.right_height += 1
                if new_node.parent.right_height <= new_node.parent.left_height:
                    break
            new_node = new_node.parent
            
        self.debugShow(label)

        if auto_rebalance:
            ## balance: parent of <current_node>
            while True:
                parent = stk.pop()
                if parent is None:
                    break
                self._balance(parent)

    #中序非递归遍历，从小到大输出所有序列
    def inorder_list_inc(self):
        s = simpleStack()
        t = self.root
        l = []
        while t is not None or not s.is_empty():
            while t is not None:
                s.push(t)
                t = t.left_child
            t = s.pop()
            l.append(t.value)
            t = t.right_child
        return l

    #中序非递归遍历，从大到小输出所有序列
    def inorder_list_dec(self):
        s = simpleStack()
        t = self.root
        l = []
        while t is not None or not s.is_empty():
            while t is not None:
                s.push(t)
                t = t.right_child
            t = s.pop()
            l.append(t.value)
            t = t.left_child
        return l

    def locate(self, value:int, root:AVLTNode|None=None)->AVLTNode|None:
        if self.root is None:
            return

        if root is None:
            node = self.root
        else:
            node = root

        while True:
            if node.value < value:
                node = node.right_child
                if node is None:
                    return
            elif node.value > value:
                node = node.left_child
                if node is None:
                    return
            else:
                return node

    def locate_min(self, node:AVLTNode|None = None)->AVLTNode:
        if node is None:
            min_node = self.root
        else:
            min_node = node
        while min_node is not None:
            if min_node.left_child:
                min_node = min_node.left_child
            else:
                break
        return min_node

    def locate_max(self, node:AVLTNode|None = None):
        if node is None:
            max_node = self.root
        else:
            max_node = node
        while max_node is not None:
            if max_node.right_child:
                max_node = max_node.right_child
            else:
                break
        return max_node

    # 找比某node更小的
    def locate_lower(self, node:AVLTNode):
        if node.left_child is not None:
            return self.locate_max(node.left_child)
        else:
            lower = node.parent
            while lower is not None and lower.value > node.value:
                lower = lower.parent
            if lower is not None and lower.value < node.value:
                return lower
            return None

    def locate_higher(self, node:AVLTNode):
        if node.right_child is not None:
            return self.locate_min(node.right_child)
        else:
            higher = node.parent
            while higher is not None and higher.value < node.value:
                higher = higher.parent
            if higher is not None and higher.value > node.value:
                return higher
            return None

    def remove(self, value:int, auto_rebalance=True):
        label = f'remove {value}'
        self.DBG(label)

        node = self.locate(value)
        if node is None:
            assert value not in self.value_list or self.value_list[value]=='r'
            self.DBG(f"{value} is not inserted or has already been removed.")
            return
        self.remove_node(node, auto_rebalance)
        self.value_list[value] = 'r'

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

        self.debugShow(label+' bef balance', check=False)
        
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
    def _balance(self, node_param:AVLTNode, recurve_to_root=False):
        node = node_param
        while node is not None:
            balance_factor = node.right_height - node.left_height
            self.DBG(f'balance({node.value}:balance_factor={balance_factor})')
            if balance_factor > 1:
                # right is heavier
                if node.right_child.balance_factor < 0: #TODO: 用<=是更严格地balance
                    # right_child.left is heavier, RL case
                    self._rl_case(node)
                elif node.right_child.balance_factor >= 0:
                    # right_child.right is heavier, RR case
                    self._rr_case(node)
            elif balance_factor < -1:
                # left is heavier
                if node.left_child.balance_factor <= 0: #TODO: 用<=是更严格地balance
                    # left_child.left is heavier, LL case
                    self._ll_case(node)
                elif node.left_child.balance_factor > 0:
                    # left_child.right is heavier, LR case
                    self._lr_case(node)
            elif not recurve_to_root:
                # Everything's fine.
                break
            node = node.parent

    # 挂载新端点
    def _hook_new_node(self, is_left:bool, new_hook:AVLTNode, parent:AVLTNode):
        if is_left is None:
            # node = self.root
            self.root = new_hook
            new_hook.parent = None
            new_hook.is_left = None
        elif is_left:
            parent.left_child = new_hook
            new_hook.parent = parent
            new_hook.is_left = True
        else:
            parent.right_child = new_hook
            new_hook.parent = parent
            new_hook.is_left = False

        assert id(new_hook.parent) ==  id(parent)

        #更新父节点左右高度值
        #TODO: more efficient，提前终止？
        while True:
            parent = new_hook.parent
            if parent is None:
                break
            is_left = new_hook.is_left
            if is_left:
                parent.left_height = max(new_hook.left_height, new_hook.right_height) + 1
            else:
                parent.right_height = max(new_hook.left_height, new_hook.right_height) + 1
            new_hook = parent
            if new_hook is None:
                break


    def _ll_case(self, child:AVLTNode):
        """Rotate Nodes for LL Case.

        Reference:
            https://en.wikipedia.org/wiki/File:Tree_Rebalancing.gif
        :return:
        """
        parent = child.parent
        is_left = child.is_left

        label = f'LL {child.value} is_left({is_left})'

        new_hook = child.left_child

        child.left_child = new_hook.right_child
        child.left_height = new_hook.right_height
        if new_hook.right_child is not None:
            new_hook.right_child.parent = child
            new_hook.right_child.is_left = True

        new_hook.right_child = child
        new_hook.right_height = max(child.right_height, child.left_height) + 1
        child.parent = new_hook
        child.is_left = False

        self._hook_new_node(is_left, new_hook, parent)

        self.debugShow(label)

    def _rr_case(self, node_param:AVLTNode):
        """Rotate Nodes for RR Case.

        Reference:
            https://en.wikipedia.org/wiki/File:Tree_Rebalancing.gif
        :return:
        """
        parent = node_param.parent
        is_left = node_param.is_left

        label = f'RR {node_param.value} is_left({is_left})'
        child = node_param
        new_hook = node_param.right_child

        child.right_child = new_hook.left_child
        child.right_height = new_hook.left_height
        if new_hook.left_child is not None:
            new_hook.left_child.parent = child
            new_hook.left_child.is_left = False

        new_hook.left_child = child
        new_hook.left_height = max(child.left_height, child.right_height) + 1
        child.parent = new_hook
        child.is_left = True

        self._hook_new_node(is_left, new_hook, parent)

        assert id(new_hook.parent) ==  id(parent)

        self.debugShow(label)

    def _lr_case(self, node:AVLTNode):
        """Rotate Nodes for LR Case.

        Reference:
            https://en.wikipedia.org/wiki/File:Tree_Rebalancing.gif
        :return:
        """
        label = f'LR {node.value}'

        child = node.left_child
        node.left_child = child.right_child
        node.left_child.parent = node
        node.left_child.is_left = True
        child.right_child = node.left_child.left_child
        child.right_height = node.left_child.left_height
        if child.right_height > 0:
            child.right_child.parent = child
            child.right_child.is_left = False

        node.left_child.left_child = child
        node.left_child.left_height = max(child.left_height, child.right_height) + 1
        child.parent = node.left_child

        node.left_height = max(node.left_child.left_height, node.left_child.right_height) + 1

        self.debugShow(label)

        self._ll_case(node)


    def _rl_case(self, node:AVLTNode):
        """Rotate Nodes for RL Case.

        Reference:
            https://en.wikipedia.org/wiki/File:Tree_Rebalancing.gif
        :return:
        """
        label = f'RL {node.value}'

        child = node.right_child
        node.right_child = child.left_child
        node.right_child.parent = node
        node.right_child.is_left = False
        child.left_child = node.right_child.right_child
        child.left_height = node.right_child.right_height
        if child.left_height > 0:
            child.left_child.parent = child
            child.left_child.is_left = True

        node.right_child.right_child = child
        node.right_child.right_height = max(child.right_height, child.left_height) + 1
        child.parent = node.right_child

        node.right_height = max(node.right_child.right_height, node.right_child.left_height) + 1

        self.debugShow(label)

        self._rr_case(node)

    def save(self):
        '''
        导出树数据
        '''
        data = []
        p = lambda x : data.append(x.save())
        preorder_nonrec(self.root, p)
        return {'nodes' : data, 'size':self.size}

    def load(self, data):
        '''
        导入树数据
        '''
        self.size = data['size']
        data = data['nodes']
        nodes = {}
        for n in data:
            new_node = AVLTNode()
            new_node.load(n)
            nodes[new_node.value] = new_node

            if new_node.parent is None:
                self.root = new_node

        def linkChild(node:AVLTNode):
            if node.left_child is not None:
                lf = nodes[node.left_child]
                node.left_child = lf
                lf.parent = node

            if node.right_child is not None:
                rt = nodes[node.right_child]
                node.right_child = rt
                rt.parent = node

        preorder_nonrec(self.root, linkChild)


