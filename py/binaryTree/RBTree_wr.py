# -*- coding: utf-8 -*-
from __future__ import annotations
import uuid
from binaryTree.absTree import TNodeInRam, TreeWithRam, NODE_BRAM
from binaryTree.util import *


import logging
RBTree_logger = logging.getLogger(__name__)


##########
# 红黑二叉树的节点
class RBTNode(TNodeInRam):
    __slots__ = [
        'parent_addr',  #指向父节点，本节点是root端点时为None
        'is_left',      #本节点是左节点还是右节点，本节点是root端点时为None
        'value',        #本节点权重值
        'left_addr',    #指向左子节点 ram地址
        'right_addr',   #    右
        'is_red',       #
        'addr',
    ]
    def __init__(self, value, is_red=True, parent_addr:None|int=None, is_left=None, left_addr:None|int=None, right_addr:None|int=None):
        super(RBTNode, self).__init__(value, parent_addr, is_left, left_addr, right_addr)
        self.is_red = is_red
    
    def __str__(self):
        s = str(self.value)
        if self.is_left is None:
            s += '(root)'
        elif self.is_left:
            s += '(L)'
        else:
            s += '(R)'
        return s

    def save(self):
        '''
        存储节点信息
        '''
        data = {}
        for item in self.__slots__:
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
            value = data[attr]
            setattr(self, attr, value)



class RBTree(TreeWithRam):
    __slots__ = [
        'root_addr',
        'stk',
        'empty_head',
        'empty_tail',
        'graphSeq',
        'ram_access_stats',
        'value_list',
        'tree_name',
        'debug_level',

        'ram',

        'size',
        'size_max',

        'graph_last',

        'logger',
        'DBG',
        'INFO',
        'WARN',
        'ERR',
    ]
    def __init__(self, name='RBTree', ram_depth=512, debug_level=0):
        '''
        debug_level:0=no-debug; 1=draw_tree; 2+=draw_tree_all
        '''
        self.ram:NODE_BRAM = None
        super(RBTree, self).__init__(name=name, ram_depth=ram_depth, debug_level=debug_level, node_impl=RBTNode)
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
        return f'RBTree({self.tree_name})'

    def _drawNode_nest(self, graph, node:RBTNode, node_tag, depth):
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
                nodelabel = str(left_child) if left_child.value is not None else 'NULL'
                fillcolor = COLORS[left_child.value  % len(COLORS)] if left_child.value is not None else 'black'    #颜色与权重绑定，保持在颜色在树平衡前后的稳定性
                linecolor = 'red' if left_child.is_red else 'black'
                graph.node(left_tag, nodelabel, style='filled', fillcolor=fillcolor, color=linecolor)    # 左节点
                graph.edge(node_tag, left_tag, label='L', fillcolor=linecolor, color=linecolor)   # 左节点与其父节点的连线
                self._drawNode_nest(graph, left_child, left_tag, depth+1)
            else:
                left_tag = str(uuid.uuid1())
                graph.node(left_tag, '', style='filled', fillcolor='white', color='white')    # 左节点
                graph.edge(node_tag, left_tag, label='', fillcolor='white', color='white')   # 左节点与其父节点的连线

            if node.right_addr is not None:
                right_child = self.ram.at(node.right_addr)
                right_tag = str(uuid.uuid1())
                nodelabel = str(right_child) if right_child.value is not None else 'NULL'
                fillcolor = COLORS[right_child.value  % len(COLORS)] if right_child.value is not None else 'black'
                linecolor = 'red' if right_child.is_red else 'black'
                graph.node(right_tag, nodelabel, style='filled', fillcolor=fillcolor, color=linecolor)
                graph.edge(node_tag, right_tag, label='R', fillcolor=linecolor, color=linecolor)
                self._drawNode_nest(graph, right_child, right_tag, depth+1)
            else:
                right_tag = str(uuid.uuid1())
                graph.node(right_tag, '', style='filled', fillcolor='white', color='white')
                graph.edge(node_tag, right_tag, label='', fillcolor='white', color='white')

    
    def check_node_valid(self, node:RBTNode):
        if node==None:
            # assert node.is_red==0
            return

        if node.is_red==1:
            assert node.left_addr==None or self.ram.at(node.left_addr).is_red==0
            assert node.right_addr==None or self.ram.at(node.right_addr).is_red==0

        if node.left_addr is not None:
            assert node.value>=self.ram.at(node.left).value and self.ram.at(node.left).is_left
            assert self.ram.at(node.left).parent_addr==node.addr
        if node.right_addr is not None:
            assert node.value<=self.ram.at(node.right).value and not self.ram.at(node.right).is_left
            assert self.ram.at(node.right).parent_addr==node.addr

    def check_valid_recur(self, node:RBTNode):
        self.check_node_valid(node)

        if node==None:
            return 1

        if node.left_addr==None and node.right_addr==None:
            if node.is_red==False:
                return 2
            else:
                return 1

        left_count = self.check_valid_recur(self.ram.at(node.left))
        right_count = self.check_valid_recur(self.ram.at(node.right))

        assert left_count==right_count

        cur_count = left_count # doesn't matter which one we choose because they're the same
        if node.is_red==0:
            cur_count += 1 

        return cur_count


    def _checkLink(self):
        assert self.ram.at(self.root_addr).is_red==0

        self.check_valid_recur(self.ram.at(self.root_addr))
    
    def _checkBalance(self):
        '''
        检查平衡性
        '''
        pass

    def _insert_helper(self, new_node:RBTNode, auto_rebalance=True):
        '''
        外部配好new_node的数据和权重即可
        '''
        label = "insert " + str(new_node.value)
        self.DBG(f'{label}...')

        new_node.left_addr = None
        new_node.right_addr = None
        new_node.is_red = True

        y = None
        x = self.root

        while x!=None:
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
        parent = node.parent
        grand = parent.parent
        while parent.is_red==1:
            if not parent.is_left:# node.parent==node.parent.parent.right:
                u = grand.left
                if u!=None and u.is_red==1:
                    u.is_red = 0
                    parent.is_red = 0
                    grand.is_red = 1
                    node = grand
                else:
                    if node.is_left:#node==node.parent.left:
                        node = parent
                        self.right_rotate(node)
                        parent = node.parent
                        grand = parent.parent
                    parent.is_red = 0
                    grand.is_red = 1
                    self.left_rotate(grand)
            else:
                u = grand.right

                if u!=None and u.is_red==1:
                    u.is_red = 0
                    parent.is_red = 0
                    grand.is_red = 1
                    node = grand
                else:
                    if not node.is_left:#node==node.parent.right:
                        node = parent
                        self.left_rotate(node)
                        parent = node.parent
                        grand = parent.parent
                    parent.is_red = 0
                    grand.is_red = 1
                    self.right_rotate(grand)
            parent = node.parent
            if parent is None:#node==self.root:
                break
            grand = parent.parent
        self.root.is_red = 0
        

    def left_rotate(self, x:RBTNode):
        '''
        总是要修改:
        x
        x.right
        若存在则要修改:
        x.right.left
        x.parent
        '''
        self.DBG(f"left_rotate")
        assert x.right_addr is not None

        y = self.ram.read(x.right_addr)
        x.right_addr = y.left_addr
        if y.left_addr!=None:
            left_child = self.ram.read(y.left_addr)
            left_child.is_left = False
            left_child.parent_addr = x.addr
            self.ram.write(left_child)

        y.parent_addr = x.parent_addr
        if x.parent_addr is None:
            y.is_left = None
            self.root_addr = y.addr
        else:
            parent = self.ram.read(x.parent_addr)
            if x.is_left:# x==x.parent.left:
                y.is_left = True
                parent.left_addr = y.addr
            else:
                parent.right_addr = y.addr
            self.ram.write(parent)

        x.is_left = True
        y.left_addr = x.addr
        x.parent_addr = y.addr
        self.ram.write(y)
        self.ram.write(x)

    def right_rotate(self, y:RBTNode):
        '''
        总是要修改:
        y
        y.left
        若存在则要修改:
        y.left.right
        y.parent
        '''
        self.DBG(f"right_rotate")

        x = self.ram.read(y.left_addr)
        y.left_addr = x.right_addr
        if x.right_addr!=None:
            right_child = self.ram.read(x.right_addr)
            right_child.is_left = True
            right_child.parent_addr = y
            self.ram.write(right_child)

        x.parent_addr = y.parent_addr
        if y.parent_addr is None:
            x.is_left = None
            self.root_addr = x.addr
        else:
            parent = self.ram.read(y.parent_addr)
            if not y.is_left:# y==y.parent.right:
                x.is_left = False
                parent.right_addr = x.addr
            else:
                parent.left_addr = x.addr
            self.ram.write(parent)
        y.is_left = False
        x.right_addr = y.addr
        y.parent_addr = x.addr
        self.ram.write(x)
        self.ram.write(y)


    # Node deletion
    def _remove_node_helper(self, node:RBTNode, auto_rebalance=True):
        z = node

        y = z
        y_original_color = y.is_red
        if z.left==None:
            # If no left child, just scoot the right subtree up
            self.__rb_transplant(z, z.right)
            if z.right!=None:
                x = z.right
            else:
                x = RBTNode(None, False)
                x.parent = z.parent
                x.is_left = z.is_left
        elif z.right==None:
            # If no right child, just scoot the left subtree up
            self.__rb_transplant(z, z.left)
            if z.left!=None:
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
                if x!=None:
                    x.parent = y
                else:
                    x = RBTNode(None, False)
                    x.is_left = False
                    x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                if y.right!=None:
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
        self.DBG('rb_transplant')

        if u.parent is None:
            self.root = v
        elif u.is_left: #u==u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v!=None:
            v.parent = u.parent
            v.is_left = u.is_left
        
    # Balancing the tree after deletion
    def delete_fix(self, x:RBTNode):
        while x!=self.root and x.is_red==0:
            self.DBG(f'delete_fix({x.value})')
            if x.is_left:# x==x.parent.left:
                s = x.parent.right
                if s!=None and s.is_red==1:
                    s.is_red = 0
                    x.parent.is_red = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if (s.left==None or s.left.is_red==0) and (s.right==None or s.right.is_red==0):
                    s.is_red = 1
                    x = x.parent
                else:
                    if s.right==None or s.right.is_red==0:
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
                if s!=None and s.is_red==1:
                    s.is_red = 0
                    x.parent.is_red = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if (s.left==None or s.left.is_red==0) and (s.right==None or s.right.is_red==0):
                    s.is_red = 1
                    x = x.parent
                else:
                    if s.left==None or s.left.is_red==0:
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

        