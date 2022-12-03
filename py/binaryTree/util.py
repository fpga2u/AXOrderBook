from tool.simpleStack import simpleStack


DBG_VIEW_ROOT = './log/binTreeView'

COLORS = ['skyblue', 'tomato', 'orange', 'purple', 'green', 'yellow', 'pink', 'aliceblue', 'aqua', 'aquamarine', 'bisque', 'blue', 'burlywood', 'cadetblue', 'chartreuse']


#先序遍历函数，主要用于树的拷贝，以及搜索前缀
#如果是文件夹，先输出文件夹名，然后再依次输出该文件夹下的所有文件(包括子文件夹)，如果有子文件夹，则再进入该子文件夹，输出该子文件夹下的所有文件名。这是一个典型的先序遍历过程。
def preorder_nonrec(t, proc):
    s = simpleStack()
    while t is not None or not s.is_empty():
        while t is not None:        # 沿左分支下行
            proc(t)            # 先根序先处理根数据
            s.push(t.right_child)         # 右分支入栈
            t = t.left_child
        t = s.pop()

#中序非递归遍历
def inorder_nonrec(t, proc):
    s = simpleStack()
    while t is not None or not s.is_empty():
        while t is not None:
            s.push(t)
            t = t.left_child
        t = s.pop()
        proc(t.value)
        t = t.right_child

#非递归的后序遍历，主要用于树的删除，以及搜索后缀
#执行操作时，肯定已经遍历过该节点的左右子节点，故适用于要进行破坏性操作的情况
#若要知道某文件夹的大小，必须先知道该文件夹下所有文件的大小，如果有子文件夹，若要知道该子文件夹大小，必须先知道子文件夹所有文件的大小。这是一个典型的后序遍历过程。
def postorder_nonrec(t, proc):
    s = simpleStack()
    while t is not None or not s.is_empty():
        while t is not None:        # 下行循环， 直到栈顶的两子树空
            s.push(t)
            t = t.left_child if t.left_child is not None else t.right_child
        t = s.pop()                 # 栈顶是应访问节点
        proc(t.value)
        if not s.is_empty() and s.top().left_child == t:
            t = s.top().right_child       # 栈不为空且当前节点是栈顶的左子节点
        else:
            t = None                # 没有右子树或右子树遍历完毕， 强迫退栈

