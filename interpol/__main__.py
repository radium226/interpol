#!/bin/env python

from .interpolate import Interpolate

import sys

def iterate_stdin():
    while True: 
        line = sys.stdin.readline()
        if line == "":
            break
        yield line
        
if __name__ == "__main__":
    interpolate = Interpolate(2, 3)
    for p in interpolate(map(lambda l: None if l == "" else int(l), map(lambda line: line.rstrip(), iterate_stdin()))):
        print("%s" % (str(p) if p is not None else ""))
