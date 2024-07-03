#!/usr/bin/env python
# coding=utf-8
import dataStruct

class executor:
    exec_list = []
    @staticmethod
    def Do():
        for op in executor.exec_list:
            try:
                op()
            except:
                print("Error happened,but I don't know where it came XD")
                print("prog has been quit,code:1")
                exit(1)
    @staticmethod
    def append(func):
        executor.exec_list.append(func)