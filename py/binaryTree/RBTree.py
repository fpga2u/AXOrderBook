# -*- coding: utf-8 -*-
from __future__ import annotations
from tkinter.tix import Tree
from graphviz import Digraph
import uuid
from tool.simpleStack import simpleStack
from binaryTree.util import *

import logging
RBTree_logger = logging.getLogger(__name__)


##########
# 红黑二叉树的节点
class RBTNode:
    __slots__ = [
        'parent',       #指向父节点，本节点是root端点时为None
        'is_left',      #本节点是左节点还是右节点，本节点是root端点时为None
        'value',        #本节点权重值，None的为NULL
        'left',         #指向左子节点
        'right',        #    右
        'is_red',       #

        #for debug view
        'host_tree',     #指向本节点所属的二叉树
    ]
    def __init__(self, value, is_red=True, parent:None|RBTNode=None, is_left=None, left:None|RBTNode=None, right:None|RBTNode=None, host_tree:None|RBTree=None):
        self.value = value  #节点在二叉树中的权重
        self.parent = parent
        self.is_left = is_left
        self.left = left
        self.right = right
        self.is_red = is_red

        self.host_tree = host_tree

    @property
    def is_root(self):
        if self.parent is None:
            assert self.is_left is None, "root with is_left not None"
        else:
            assert self.is_left is not None, "none-root with is_left is None"
        return self.parent is None

    def printTree(self):
        '''
        利用Graphviz实现二叉树的可视化
        '''
        # colors for labels of nodes
        graph = Digraph(comment='RB Binary Tree')

        def printNode(node:RBTNode, node_tag):
            '''
            绘制以某个节点为根节点的二叉树
            '''
            if node.left is None and node.right is None:
                return
            # 节点颜色
            if node.left is not None:
                left_tag = str(uuid.uuid1())
                nodelabel = str(node.left) if node.left.value is not None else 'NULL'
                fillcolor = COLORS[node.left.value  % len(COLORS)] if node.left.value is not None else 'black'    #颜色与权重绑定，保持在颜色在树平衡前后的稳定性
                linecolor = 'red' if node.left.is_red else 'black'
                graph.node(left_tag, nodelabel, style='filled', fillcolor=fillcolor, color=linecolor)    # 左节点
                graph.edge(node_tag, left_tag, label='L', fillcolor=linecolor, color=linecolor)   # 左节点与其父节点的连线
                printNode(node.left, left_tag)
            else:
                left_tag = str(uuid.uuid1())
                graph.node(left_tag, '', style='filled', fillcolor='white', color='white')    # 左节点
                graph.edge(node_tag, left_tag, label='', fillcolor='white', color='white')   # 左节点与其父节点的连线

            if node.right is not None:
                right_tag = str(uuid.uuid1())
                nodelabel = str(node.right) if node.right.value is not None else 'NULL'
                fillcolor = COLORS[node.right.value  % len(COLORS)] if node.right.value is not None else 'black'
                linecolor = 'red' if node.right.is_red else 'black'
                graph.node(right_tag, nodelabel, style='filled', fillcolor=fillcolor, color=linecolor)
                graph.edge(node_tag, right_tag, label='R', fillcolor=linecolor, color=linecolor)
                printNode(node.right, right_tag)
            else:
                right_tag = str(uuid.uuid1())
                graph.node(right_tag, '', style='filled', fillcolor='white', color='white')
                graph.edge(node_tag, right_tag, label='', fillcolor='white', color='white')

        # 如果树非空
        if self.value is not None:
            root_tag = str(uuid.uuid1())                # 根节点标签
            fillcolor = COLORS[self.value  % len(COLORS)]
            graph.node(root_tag, str(self), style='filled', fillcolor=fillcolor, color='black')     # 创建根节点
            printNode(self, root_tag)

        return graph
    
    def __str__(self):
        s = str(self.value)
        if self.is_left is None:
            s += '(root)'
        elif self.is_left:
            s += '(L)'
        else:
            s += '(R)'
        return s#f'RBTNode({self.value}) id:{id(self)}'

    def save(self):
        '''
        存储节点信息
        '''
        data = {}
        for item in self.__slots__:
            if item in ['host_tree']:
                continue
            attr = getattr(self, item)
            if isinstance(attr, RBTNode):
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
            if attr in ['host_tree']:
                continue
            value = data[attr]
            setattr(self, attr, value)



class RBTree:
    NULL_NODE = None #RBTNode(None, False)
    def __init__(self, name='RBTree', debug_level=0):
        '''
        debug_level:0=no-debug; 1=draw_tree; 2+=draw_tree_all
        '''
        self.root = RBTree.NULL_NODE
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
        RBTree_logger.setLevel(g_logger.getEffectiveLevel())
        for h in g_logger.handlers:
            self.logger.addHandler(h)
            RBTree_logger.addHandler(h) #这里补上模块日志的handler

        self.DBG = self.logger.debug
        self.INFO = self.logger.info
        self.WARN = self.logger.warning
        self.ERR = self.logger.error

    def __str__(self):
        return f'RBTree({self.tree_name}) id:{id(self)}'

    #打印树 #for debug only
    def debugShow(self, label="", check=True):
        self.DBG(f"show {label}")
        if not self.root:
            self.DBG(f" Tree is empty!")
            return
        if self.debug_level>0:
            graph = self.root.printTree()
            if self.debug_level>1:    #显示上一步和当前
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

    
    def check_node_valid(self, node:RBTNode):
        if node==RBTree.NULL_NODE:
            # assert node.is_red==0
            return

        if node.is_red==1:
            assert node.left==RBTree.NULL_NODE or node.left.is_red==0
            assert node.right==RBTree.NULL_NODE or node.right.is_red==0

        if node.left!=RBTree.NULL_NODE and node.left is not None:
            assert node.value>=node.left.value and node.left.is_left
            assert node.left.parent==node
        if node.right!=RBTree.NULL_NODE and node.right is not None:
            assert node.value<=node.right.value and not node.right.is_left
            assert node.right.parent==node

    def check_valid_recur(self, node:RBTNode):
        self.check_node_valid(node)

        if node==RBTree.NULL_NODE:
            return 1

        if node.left==RBTree.NULL_NODE and node.right==RBTree.NULL_NODE:
            if node.is_red==0:
                return 2
            else:
                return 1

        left_count = self.check_valid_recur(node.left)
        right_count = self.check_valid_recur(node.right)

        assert left_count==right_count

        cur_count = left_count # doesn't matter which one we choose because they're the same
        if node.is_red==0:
            cur_count += 1 

        return cur_count


    def _checkTree(self):
        assert self.root.is_red==0

        self.check_valid_recur(self.root)
    
    def insert(self, new_node:RBTNode, auto_rebalance=True):
        label = "insert " + str(new_node.value)
        self.DBG(f'{label}...')

        new_node.parent = None
        new_node.left = RBTree.NULL_NODE
        new_node.right = RBTree.NULL_NODE
        new_node.is_red = True

        y = None
        x = self.root

        while x!=RBTree.NULL_NODE:
            y = x
            if new_node.value<x.value:
                x = x.left
            else:
                x = x.right

        new_node.parent = y
        if y is None:
            self.root = new_node
        elif new_node.value<y.value:
            new_node.is_left = True
            y.left = new_node
        else:
            new_node.is_left = False
            y.right = new_node
        
        self.size += 1
        if self.size>self.size_max:
            self.size_max = self.size

        if new_node.parent is None:
            new_node.is_red = False
            self.debugShow(label)
            return

        if new_node.parent.parent is None:
            self.debugShow(label)
            return

        if auto_rebalance:
            self._balance(new_node)

        self.debugShow(label)

    # Balance the tree after insertion
    def _balance(self, node:RBTNode):
        while node.parent.is_red==1:
            if node.parent==node.parent.parent.right:
                u = node.parent.parent.left
                if u!=RBTree.NULL_NODE and u.is_red==1:
                    u.is_red = 0
                    node.parent.is_red = 0
                    node.parent.parent.is_red = 1
                    node = node.parent.parent
                else:
                    if node==node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.is_red = 0
                    node.parent.parent.is_red = 1
                    self.left_rotate(node.parent.parent)
            else:
                u = node.parent.parent.right

                if u!=RBTree.NULL_NODE and u.is_red==1:
                    u.is_red = 0
                    node.parent.is_red = 0
                    node.parent.parent.is_red = 1
                    node = node.parent.parent
                else:
                    if node==node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.is_red = 0
                    node.parent.parent.is_red = 1
                    self.right_rotate(node.parent.parent)
            if node==self.root:
                break
        self.root.is_red = 0
        

    def left_rotate(self, x:RBTNode):
        y = x.right
        x.right = y.left
        if y.left!=RBTree.NULL_NODE:
            y.left.is_left = False
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            y.is_left = None
            self.root = y
        elif x.is_left:# x==x.parent.left:
            y.is_left = True
            x.parent.left = y
        else:
            x.parent.right = y
        x.is_left = True
        y.left = x
        x.parent = y

    def right_rotate(self, x:RBTNode):
        y = x.left
        x.left = y.right
        if y.right!=RBTree.NULL_NODE:
            y.right.is_left = True
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            y.is_left = None
            self.root = y
        elif not x.is_left:# x==x.parent.right:
            y.is_left = False
            x.parent.right = y
        else:
            x.parent.left = y
        x.is_left = False
        y.right = x
        x.parent = y


    #中序非递归遍历，从小到大输出所有序列
    def inorder_list_inc(self):
        s = simpleStack()
        t = self.root
        l = []
        while t is not None or not s.is_empty():
            while t is not None:
                s.push(t)
                t = t.left
            t = s.pop()
            l.append(t.value)
            t = t.right
        return l

    #中序非递归遍历，从大到小输出所有序列
    def inorder_list_dec(self):
        s = simpleStack()
        t = self.root
        l = []
        while t is not None or not s.is_empty():
            while t is not None:
                s.push(t)
                t = t.right
            t = s.pop()
            l.append(t.value)
            t = t.left
        return l

    def locate(self, value:int)->RBTNode|None:
        if self.root is None:
            return

        node = self.root
        while True:
            if node.value<value:
                node = node.right
                if node is None:
                    return
            elif node.value>value:
                node = node.left
                if node is None:
                    return
            else:
                return node


    def locate_min(self, node:RBTNode|None = None)->RBTNode:
        if node is None:
            min_node = self.root
        else:
            assert id(node.host_tree)== id(self)
            min_node = node
        while min_node is not None:
            if min_node.left:
                min_node = min_node.left
            else:
                break
        return min_node

    def locate_max(self, node:RBTNode|None = None):
        if node is None:
            max_node = self.root
        else:
            assert id(node.host_tree)== id(self)
            max_node = node
        while max_node is not None:
            if max_node.right:
                max_node = max_node.right
            else:
                break
        return max_node

    # 找比某node更小的
    def locate_lower(self, node:RBTNode):
        assert id(node.host_tree)== id(self)
        if node.left is not None:
            return self.locate_max(node.left)
        else:
            lower = node.parent
            while lower is not None and lower.value>node.value:
                lower = lower.parent
            if lower is not None and lower.value<node.value:
                return lower
            return None
            
    def locate_higher(self, node:RBTNode):
        assert id(node.host_tree)== id(self)
        if node.right is not None:
            return self.locate_min(node.right)
        else:
            higher = node.parent
            while higher is not None and higher.value<node.value:
                higher = higher.parent
            if higher is not None and higher.value>node.value:
                return higher
            return None

    def remove(self, value:int, auto_rebalance=True):
        label = "remove " + str(value)
        self.DBG(f'{label}...')
        if value==19:
            value =19
        self.delete_node_helper(self.root, value, auto_rebalance)
        self.debugShow(label)

    # Node deletion
    def delete_node_helper(self, node:RBTNode|None, key, auto_rebalance=True):
        z = RBTree.NULL_NODE
        while node!=RBTree.NULL_NODE:
            if node.value==key:
                z = node

            if node.value<=key:
                node = node.right
            else:
                node = node.left

        if z==RBTree.NULL_NODE:
            # print("Cannot find key in the tree")
            return

        y = z
        y_original_color = y.is_red
        if z.left==RBTree.NULL_NODE:
            # If no left child, just scoot the right subtree up
            self.__rb_transplant(z, z.right)
            if z.right!=RBTree.NULL_NODE:
                x = z.right
            else:
                x = RBTNode(None, False)
                x.parent = z.parent
                x.is_left = z.is_left
        elif z.right==RBTree.NULL_NODE:
            # If no right child, just scoot the left subtree up
            self.__rb_transplant(z, z.left)
            if z.left!=RBTree.NULL_NODE:
                x = z.left
            else:
                x = RBTNode(None, False)
                x.parent = z.parent
                x.is_left = z.is_left
        else:
            y = self.locate_min(z.right)
            y_original_color = y.is_red
            if y.parent==z:
                x = y.right
                if x!=RBTree.NULL_NODE:
                    x.parent = y
                else:
                    x = RBTNode(None, False)
                    x.is_left = False
                    x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                if y.right!=RBTree.NULL_NODE:
                    x = y.right
                else:
                    x = RBTNode(None, False)
                    x.parent = y.parent
                    x.is_left = y.is_left
                y.right = z.right
                y.right.parent = y
            

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.is_red = z.is_red
        if y_original_color==0 and self.root is not None and auto_rebalance:
            self.delete_fix(x)

        self.size -= 1
        
    def __rb_transplant(self, u:RBTNode, v:RBTNode):
        if u.parent is None:
            self.root = v
        elif u.is_left: #u==u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v!=RBTree.NULL_NODE:
            v.parent = u.parent
            v.is_left = u.is_left
        
    # Balancing the tree after deletion
    def delete_fix(self, x:RBTNode):
        # print(x.item, x==self.TNULL, x is None, self.size, x.parent, x.parent.left, x.parent.right, x.parent.right.left, x.parent.right.right)
        # if x.parent.right.right is None:
        #     self.print_tree()
        while x!=self.root and x.is_red==0:
            if x.is_left:# x==x.parent.left:
                s = x.parent.right
                if s!=RBTree.NULL_NODE and s.is_red==1:
                    s.is_red = 0
                    x.parent.is_red = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if (s.left==RBTree.NULL_NODE or s.left.is_red==0) and (s.right==RBTree.NULL_NODE or s.right.is_red==0):
                    s.is_red = 1
                    x = x.parent
                else:
                    if s.right==RBTree.NULL_NODE or s.right.is_red==0:
                        s.left.is_red = 0
                        s.is_red = 1
                        self.right_rotate(s)
                        s = x.parent.right

                    s.is_red = x.parent.is_red
                    x.parent.is_red = 0
                    s.right.is_red = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s!=RBTree.NULL_NODE and s.is_red==1:
                    s.is_red = 0
                    x.parent.is_red = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if (s.left==RBTree.NULL_NODE or s.left.is_red==0) and (s.right==RBTree.NULL_NODE or s.right.is_red==0):
                    s.is_red = 1
                    x = x.parent
                else:
                    if s.left==RBTree.NULL_NODE or s.left.is_red==0:
                        s.right.is_red = 0
                        s.is_red = 1
                        self.left_rotate(s)
                        s = x.parent.left

                    s.is_red = x.parent.is_red
                    x.parent.is_red = 0
                    s.left.is_red = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.is_red = 0