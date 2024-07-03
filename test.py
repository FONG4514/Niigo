#!/usr/bin/env python
# coding=utf-8
import dataStruct
import time


start = time.perf_counter()
a = 1+2
b = 4*5
c = 4+5
a = a+b
print(a)
a = a*b
print(c)
end = time.perf_counter()
print(f"total time cost:{(end - start) * 1000:.3f}ms")
