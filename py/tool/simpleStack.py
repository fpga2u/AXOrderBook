
class simpleStack(object):
    def __init__(self):
        # 创建空列表实现栈
        self.__list = []
        self.max_size = 0

    def is_empty(self):
        # 判断是否为空
        return self.__list == []

    def push(self,item):
        # 压栈，添加元素
        self.__list.append(item)
        if len(self.__list) > self.max_size:
            self.max_size = len(self.__list)

    def pop(self):
        # 弹栈，弹出最后压入栈的元素
        if self.is_empty():
            return 
        else:
            return self.__list.pop()

    def top(self): 
        # 取最后压入栈的元素
        if self.is_empty():
            return
        else:
            return self.__list[-1]