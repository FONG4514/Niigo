#!/usr/bin/env python
# coding=utf-8
import analyzer
import const

'''
这个模块包含了Niigo的主要数据结构，例如主要栈，符号表，函数表等
'''


class main_stack:
    """
    这个是标准主要栈，其容量当前默认为32个内容，支持入栈，出栈，根据index替换
    """

    lenght = const.STACK_LEN
    stack = []
    count = 0

    @staticmethod
    def __int__():
        main_stack.stack = []

    @staticmethod
    def pop(self):
        main_stack.stack.pop()
        self.count -= 1

    @staticmethod
    def remove(index):
        main_stack.stack.pop(index)

    @staticmethod
    def push(ele):
        if main_stack.lenght - 1 == 0:
            print("Error happened:Too many element in Array")
            print("prog has been quit,code:666")
            exit(666)
        main_stack.stack.append(ele)
        main_stack.lenght -= 1

    @staticmethod
    def get_var(index):
        try:
            return main_stack.stack[index]
        except:
            print(f'Error happened:Index outboard in line:{analyzer.count_line}')
            exit(1)

    @staticmethod
    def update(index,new_ele):
        main_stack.stack[index] = new_ele


class func_table:
    """
    这个是函数表，用于读入函数后将子流程保存在字典里，方便以后调用
    """

    table = {}

    @staticmethod
    def add_func(func_name, func):
        func_table.table[func_name] = func
        return True

    @staticmethod
    def find_func(func_name):
        func = func_table.table[func_name]
        return func


class subProcess:
    """
    这个是子流程，用于保存运行过程到一个列表，这个类不是单例的
    """
    def __int__(self):
        self.exec_list = []
        self.symbol_table = {}


def point_for_new_var(value,expr):
    if expr is not None:
        res = calu_symbol.evaluate_rpn(expr)
        main_stack.push(res)
    else:
        main_stack.push(value)


def delete_var(value):
    main_stack.remove(value)


def use_var(index):
    var = main_stack.get_var(index)
    return var


def loop(times, func_list):
    pass


def return_result():
    pass


def inputToStack(offset):
    print("please input something:")
    main_stack.stack[offset] = input()


def outputFormStack(ele,expr):
    print(main_stack.stack[ele])

def outputDirectly(ele,expr):
    if expr is not None:
        res = calu_symbol.evaluate_rpn(expr)
        print(res)
    else:
        print(ele)

def updateStack(index,new_ele,expr):
    if expr is not None:
        res = calu_symbol.evaluate_rpn(expr)
        main_stack.update(index, res)
    else:
        main_stack.update(index, new_ele)

class symbol_table:
    table = {
        "new": point_for_new_var,
        "delete": delete_var,
        "use": use_var,
        "loop": loop,
        "re": return_result,
        "in": inputToStack,
        "out": outputFormStack,
        "dout":outputDirectly,
        "update":updateStack,
    }


class calu_symbol:
    """
    这个类用于一些计算，比如默认支持的逆波兰表达式和布尔运算
    """
    #TODO BUG:再将数字放回主要栈的时候，是number类型，但是下面却需要string类型，因此报错
    @staticmethod
    def evaluate_rpn(expression: str) -> int:
        """
        这个函数用于计算逆波兰表达式
        :param expression: 一个逆波兰表达式除了最后一个元素，其余使用#分隔
        :return: 返回计算结果，一个整数
        """
        # 将表达式按#分割成列表
        try:
            tokens = expression.split('#')
            i = 0
            while i < len(tokens):
                if tokens[i].startswith("[[") and tokens[i].endswith("]]"):
                    ele = tokens[i][2:-2]
                    int_ele = int(ele)
                    tokens[i] = main_stack.stack[int_ele]
                i += 1

            stack = []
            # 遍历每个token
            for token in tokens:
                new_t = str(token)
                if new_t.isdigit():
                    if isinstance(new_t,str):
                        stack.append(int(new_t))
                    else:
                        stack.append(new_t)
                else:
                    b = stack.pop()
                    a = stack.pop()
                    if token == '+':
                        stack.append(a + b)
                    elif token == '-':
                        stack.append(a - b)
                    elif token == '*':
                        stack.append(a * b)
                    elif token == '/':
                        stack.append(int(a / b))
            return stack[0]
        except Exception:
            print(f"Error happened:bad expr in line {analyzer.count_line}")
            exit(1)

    @staticmethod
    def evaluate_bool(A,B):
        pass
