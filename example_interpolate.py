#!/bin/env python

import random
import subprocess
from interpolate import Interpolate

random.seed()

GNUPLOT = [
        "set style line 1 lc rgb '#0060ad' lt 1 lw 2 pt 7 ps 1.5", 
        "set style line 2 lc rgb '#dd181f' lt 1 lw 2 pt 5 ps 1.5", 
        "plot for [i=0:1] './interpolate.plt' index i with linespoints ls (i+1)"
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
        return 10 + x**4 + x**3 - 20 * x**2

    data = []
    while len(data) < size:
        missing = random_int(0, 2) == 0
        length = random_int(2, 3) #random_int(5, 10))
        data += list(map(lambda x: f(x) if not missing else None, list(range(len(data), len(data) + length))))
    return enumerate(data[0:size])

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
    interpolate = Interpolate(1, 3, 1)
    data = list(sample(100))
    print(data)
    interpolated_data = list(interpolate(data))
    print(interpolated_data)
    data_1 = map(lambda pair: pair if pair[1] is not None else None, data)
    data_2 = filter(lambda p: p is not None and p[1] is not None, map(lambda pair: pair[1] if pair[0][1] is None else None, zip(data, interpolated_data)))
    fd = open("./interpolate.plt", "w+")
    #gnuplot = subprocess.Popen(["gnuplot", "-p", "-e", "; ".join(GNUPLOT)], stdin=subprocess.PIPE)
    write_data(fd, data_1, "present")
    fd.write("\n\n") #bytearray("\n\n", "utf-8"))
    write_data(fd, data_2, "interpolated")
    fd.close()
    gnuplot = subprocess.Popen(["gnuplot", "-p", "-e", "; ".join(GNUPLOT)], stdin=subprocess.PIPE)
    #print(list(data_2))
    
