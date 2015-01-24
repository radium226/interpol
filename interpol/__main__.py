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
    interpolate = Interpolate(1, 100, 1)
    for p in interpolate(enumerate(map(lambda l: None if l == "" else float(l), map(lambda line: line.rstrip(), iterate_stdin())))):
        print("%i" % p[1])
        
