#!/bin/env python

from collections import deque as Deque
import itertools
from scipy.interpolate import InterpolatedUnivariateSpline
from .ring import PartitionedRing
 
# https://github.com/tyarkoni/transitions

class Interpolate(object):

    def __init__(self, interpolable_max_length):
        self.__ring = PartitionedRing(items=2 + 2 + interpolable_max_length, partitions=3, boundary=lambda left, right: left is None and right is not None or left is not None and right is None)
        self.__interpolable_max_length = interpolable_max_length
        self.__startup_min_length = 2
    def __interpolate(self, pairs):
        #def linear_interpolator(a, b):
        #    x_a, y_a = a
        #    x_b, y_b = b
        #    def f(x):
        #        return (x_b - x) / (x_b - x_a) * y_a + (x - x_a) / (x_b - x_a) * y_b
        #    return f
        before, between, after = self.__partition_ring()
        #print(before)
        #print(between)
        #print(after)
        #a = before[-1]
        #b = after[0]
        #f = linear_interpolator(a, b)
        known_x = list(map(lambda p: p[0], before + after))
        known_y = list(map(lambda p: p[1], before + after))
        #print(x)
        #print(y)
        interpolator = InterpolatedUnivariateSpline(known_x, known_y, k=min(5, (len(before) + len(after)) // 2))
        
        return before + [(x, interpolator(x).item()) for x in map(lambda pair: pair[0], between)] + after
    
    def __iterate(self, appened_item, maybe_ejected):
        def is_absent(item):
            return item is None

        def is_present(item):
            return item is not None

        def all_absent(partition):
            return all(map(lambda pair: pair is None, partition))

        def all_present(partition):
            return all(map(lambda pair: pair is not None, partition))

        if maybe_ejected.is_something():
            either_ejected = maybe_ejected.value
            if either_ejected.is_left():  # item
                ejected_item = either_ejected.value
            elif either_ejected.is_right():
                ejected_partition = either_ejected.value
            else:
                raise AssertionError

        if len(self.__ring.partitions) == 1:
            (single_partition) = self.__ring.partitions
            if maybe_ejected.is_nothing():
                if all_absent(single_partition):
                    yield appened_item # We are fucked anyway
                elif all_present(single_partition):
                    yield appened_item # Let's go on
                else:
                    raise AssertionError
            elif maybe_ejected.is_something():
                either_ejected = maybe_ejected.value
                if either_ejected.is_left():
                    ejected_item = either_ejected.value
                    yield appened_item # We are continuing a serie of ongoing absent / present item
                else:
                    ejected_partition = maybe_ejected.value
                    yield appened_item
                        
        else:
            raise AssertionError


        
    
    def __call__(self, iterator):
        for item in iterator:
            maybe = self.__ring.append(item)
            yield from self.__iterate(item, maybe)


