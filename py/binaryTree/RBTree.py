# -*- coding: utf-8 -*-
from __future__ import annotations
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
    def __init__(self, value, is_red, parent:None|RBTNode=None, is_left=None, left:None|RBTNode=None, right:None|RBTNode=None, host_tree:None|RBTree=None):
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
                nodelabel = str(node.left.value) if node.left.value is not None else 'NULL'
                fillcolor = COLORS[node.left.value  % len(COLORS)]    #颜色与权重绑定，保持在颜色在树平衡前后的稳定性
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
                nodelabel = str(node.right.value) if node.left.value is not None else 'NULL'
                fillcolor = COLORS[node.right.value  % len(COLORS)]
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
            graph.node(root_tag, str(self.value), style='filled', fillcolor=fillcolor, color='black')     # 创建根节点
            printNode(self, root_tag)

        return graph

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
    NULL_NODE = RBTNode(-1, False)
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
        self.DBG(f"{label}")
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
        if node == RBTree.NULL_NODE:
            assert node.is_red == 0
            return

        if node.is_red == 1:
            assert node.left.is_red == 0
            assert node.right.is_red == 0

        if node.left != RBTree.NULL_NODE and node.left is not None:
            assert node.item >= node.left.item
        if node.right != RBTree.NULL_NODE and node.right is not None:
            assert node.item <= node.right.item


    def check_valid_recur(self, node:RBTNode):
        self.check_node_valid(node)

        if node == RBTree.NULL_NODE:
            return 1

        if node.left == RBTree.NULL_NODE and node.right == RBTree.NULL_NODE:
            if node.is_red == 0:
                return 2
            else:
                return 1

        left_count = self.check_valid_recur(node.left)
        right_count = self.check_valid_recur(node.right)

        assert left_count == right_count

        cur_count = left_count # doesn't matter which one we choose because they're the same
        if node.is_red == 0:
            cur_count += 1 

        return cur_count


    def _checkTree(self):
        assert self.root.is_red == 0

        self.check_valid_recur(self.root)