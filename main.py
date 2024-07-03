#!/usr/bin/env python
# coding=utf-8
import analyzer
import dataStruct
from executor import executor
import time


def main():
    start = time.perf_counter()
    with open("./script.ds", "r") as f:
        for line in f:
            analyzer.analyzer_line(line)
        print(f"compile complete! Now start run! total line:{analyzer.count_line}")
        executor.Do()
    end = time.perf_counter()
    print(f"total time cost:{(end-start)*1000:.3f}ms")

if __name__ == "__main__":
    main()
