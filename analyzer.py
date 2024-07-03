#!/usr/bin/env python
# coding=utf-8
import dataStruct
from functools import partial
import executor
import const

'''
这个模块包含了语法解析器，Niigo脚本语言是以行为规范的语言，因此脚本是按行解析
'''

#  count_line用来记录当前读取到多少行
count_line = 0


def analyzer_line(line):
    """
    这个函数用于解析每一行的语法，先拆分一行,然后根据情况加入主要栈或者执行队列
    :param line:一行输入,里面包含一行的语法:
    :return:
    """
    global count_line
    count_line += 1
    line.replace("\n", "")
    words = line.split()
    for word in words:
        if word == '.':
            # 解析到.的情况，分别去除内容，交给处理函数
            for index in words[1:]:
                push_or_update_stack(index)
        elif word == 'out':
            # 解析到关键字out的情况，out是从标准主要栈里面获取一个内容并且使用标准输出打印
            # 获得到后续除了out的内容，然后从[[]]或者直接打印字面值
            for index in words[1:]:
                solve_out(index)
        elif word == 'in':
            # 解析到关键字in的情况，in是等待用户输入
            # 由于Niigo语言是先解析后执行，in是执行期标识符，因此要先记录当前offset并且塞入一个None占位，然后将偏移量传入符号表对应的in处理
            # 当执行期时，得到用户输入后就可以替换None
            offset = len(dataStruct.main_stack.stack)
            dataStruct.main_stack.stack.insert(offset, None)
            exec = partial(dataStruct.symbol_table.table["in"], offset)
            executor.executor.append(exec)
            dataStruct.main_stack.count+=1


def use_element(index):
    """
    这个函数用于解析[[]]，包含了里面是字面值或者表达式的情况
    :param index:这里的名字取的很不好，这个index是一串[[]]表达式
    :return: int_ele/int_num:这两个其实是一个东西，都是对[[]]的内容解析出来的数字，其中数字来源有字面值或者波兰表达式
    """
    if index.startswith('[[') and index.endswith(']]'):
        ele = index[2:-2]
        if ele.startswith('((') and ele.endswith('))'):
            num = dataStruct.calu_symbol.evaluate_rpn(ele[2:-2])
            try:
                int_num = int(num)
            except:
                print("error happened:Type error")
            return int_num

        try:
            int_ele = int(ele)
        except:
            print("error happened:Type error")
        return int_ele


def analyzer_double_parentheses(line):
    """
    这个函数用于处理(())情况，即计算括号内的逆波兰表达式
    :param line: 包含(())的表达式
    :return: 计算结果
    """
    if line.startswith("((") and line.endswith("))"):
        num = dataStruct.calu_symbol.evaluate_rpn(line[2:-2])
        return num


def push_or_update_stack(line):
    """
    这个处理.关键字的参数，.关键字有两种用法，一种是例如. HelloWorld创建新变量
    另外一种是 . [[0]]?ttteeeexxxxtttt 这种覆盖之前的元素
    这个函数是逐个解析加入列表,而且是在运行期更新,创建初始数据则是在解释期创建
    不可以对没有开辟的栈进行[[]]?的修改操作
    :param line: .后的表达式列表的其中一个表达式
    :return:
    """
    if line.startswith("[["):
        tokens = line.split('?')
        res = use_element(tokens[0])
        check_broad_line(res)
        if tokens[1].startswith("((") and tokens[1].endswith("))"):
            exec = partial(dataStruct.symbol_table.table["update"], index=res, new_ele=0,expr=tokens[1][2:-2])
            executor.executor.append(exec)
        else:
            # 这个是用字面值进行修改的
            exec = partial(dataStruct.symbol_table.table["update"], index=res, new_ele=tokens[1],expr = None)
            executor.executor.append(exec)

    elif line.startswith("((") and line.endswith("))"):
        exec = partial(dataStruct.symbol_table.table["new"], value=None,expr=line[2:-2])
        executor.executor.append(exec)
        dataStruct.main_stack.count += 1
    else:
        exec = partial(dataStruct.main_stack.push, line)
        executor.executor.append(exec)
        dataStruct.main_stack.count += 1

def solve_out(index):
    if index.startswith("[[") and index.endswith("]]"):
        # 这个是使用[[]]的情况,即从标准主要栈获取元素
        var = use_element(index)
        #给out做边界检查防止越界
        check_broad_line(var)
        if var is not None:
            exec = partial(dataStruct.symbol_table.table["out"], var,expr = None)
            executor.executor.append(exec)
    elif index.startswith("((") and index.endswith("))"):
        exec = partial(dataStruct.symbol_table.table["dout"], res=None,expr=index[2:-2])
        executor.executor.append(exec)
    else:
        # 这个是打印字面值的情况
        exec = partial(dataStruct.symbol_table.table["dout"], ele=index,expr=None)
        executor.executor.append(exec)


def check_broad_line(index):
    if dataStruct.main_stack.count <= index:
        print(f"Error happened:try using unaccess stack area in line:{count_line}")
        exit(3)