#!/bin/env python

import random
import subprocess
from interpolate import Interpolate
from math import sin, cos

PI = 3.1415

random.seed()

GNUPLOT = [
        "reset", 
        "unset border", 
        "unset xtics", 
        "unset ytics", 
        "set terminal pngcairo size 400,300 enhanced", 
        "set output 'example_interpolate.png'",
        "set style line 1 lc rgb '#0060ad' lt 0 lw 0 pt 5 ps 0.5", 
        "set style line 2 lc rgb '#dd181f' lt 0 lw 0 pt 5 ps 0.5",
        "plot for [i=0:1] './example_interpolate.dat' index i notitle with linespoints ls (i+1)"
    ]

SAMPLE = [
"# plotting_data1.dat", 
"# X   Y", 
"  1   2", 
"  2   3", 
"  3   2", 
"  4   1"    ]

def random_int(a, b):
    return random.randint(a, b)

def sample(size):
    def f(x):
        return x * cos(x)

    return list(enumerate(map(lambda y: None if random_int(0, 3) == 0 else y,[f(x / 10) for x in range(- size // 2, size // 2)])))


def write_data(fd, data, label):
    text = ""
    can_break = True
    for datum in data:
        if datum is None:
            if can_break:
                text += "\n"
                can_break = False
        else:
            text += "%s %s\n" % (repr(datum[0]), repr(datum[1]))
            can_break = True
    fd.write(text) #bytearray(text, "utf-8"))

if __name__ == "__main__":
    interpolate = Interpolate(1, 50, 1)
    data = list(sample(50))
    interpolated_data = list(interpolate(data))
    data_1 = map(lambda pair: pair if pair[1] is not None else None, data)
    data_2 = map(lambda pair: pair if pair is not None and pair[1] is not None else None, map(lambda pair: pair[1] if pair[0][1] is None else None, zip(data, interpolated_data)))
    fd = open("./example_interpolate.dat", "w+")
    #gnuplot = subprocess.Popen(["gnuplot", "-p", "-e", "; ".join(GNUPLOT)], stdin=subprocess.PIPE)
    write_data(fd, data_1, "present")
    fd.write("\n\n") #bytearray("\n\n", "utf-8"))
    write_data(fd, data_2, "interpolated")
    fd.close()
    #print(list(data_2))
    gnuplot = subprocess.Popen(["gnuplot", "-p", "-e", "; ".join(GNUPLOT)], stdin=subprocess.PIPE)
