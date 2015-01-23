#!/bin/env python

import random
import subprocess
from interpolate import Interpolate

random.seed()

GNUPLOT = [
        "set xrange[0:20]", 
        "set style line 1 lc rgb '#0060ad' lt 1 lw 2 pt 7 ps 1.5", 
        "set style line 2 lc rgb '#dd181f' lt 1 lw 2 pt 5 ps 1.5", 
        "plot '-' index 0 with linespoints ls 1, '-'  index 1 with linespoints ls 2"
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
        return x**4 + x**3 - 20 * x**2

    data = []
    while len(data) < size:
        missing = random_int(0, 2) == 0
        length = random_int(2, 3) #random_int(5, 10))
        data += map(lambda x: (x, f(x)) if not missing else (x, None), list(range(len(data), len(data) + length)))
    return data[0:size]

def plot_data(gnuplot, data, label):
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
    print(label)
    print(text)
    gnuplot.stdin.write(bytearray(text, "utf-8"))

if __name__ == "__main__":
    interpolate = Interpolate(1, 5, 1)
    data = sample(20)
    interpolated_data = interpolate(data)

    data_1 = map(lambda pair: pair if pair[1] is not None else None, data)
    data_2 = map(lambda pair: pair[1] if pair[0][1] is None else None, zip(data, interpolated_data))

    gnuplot = subprocess.Popen(["gnuplot", "-p", "-e", "; ".join(GNUPLOT)], stdin=subprocess.PIPE)
    plot_data(gnuplot, data_1, "present")
    gnuplot.stdin.write(bytearray("\n\n\n", "utf-8"))
    plot_data(gnuplot, data_2, "interpolated")
    
