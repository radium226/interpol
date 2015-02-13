#!/bin/env python

from collections import deque as Deque
import itertools
from scipy.interpolate import InterpolatedUnivariateSpline
from .ring import PartitionedRing
 
# https://github.com/tyarkoni/transitions

class Interpolate(object):

    def __init__(self, min_present_item_count=2, max_absent_item_count=4, absent_item_matcher=lambda item: item is None):
        self.__min_present_item_count = min_present_item_count
        self.__max_absent_item_count = max_absent_item_count
        self.__is_item_absent = absent_item_matcher
        
        self.__ring = PartitionedRing(max_partition_count=3, max_item_count=2 * min_present_item_count + max_absent_item_count, boundary_matcher=self.__is_item_boundary)
    
    def __is_item_boundary(self, left_item, right_item):
        return self.__is_item_absent(left_item) and not self.__is_item_absent(right_item) or not self.__is_item_absent(left_item) and self.__is_item_absent(right_item)
    
    def __are_items_absent(self, items):
        return all(map(lambda item: self.__is_item_absent(item), items))
    
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
    
    @property
    def __partitions(self):
        return self.__ring.partitions
    
    def __iterate(self, appened_item, maybe_ejected):
        print("appened_item=" + repr(appened_item) + "\t\tmaybe_ejected=" + repr(maybe_ejected) + "\t\tpartitions = " + repr(self.__partitions))
         # We should do something because it seems that we can interpolate, dude! 
        if len(partitions) == 3:
            if len(partitions[0]) >= self.__before_size:
                assert len(partitions[1]) <= self.__interpolatable_size
                if len(partitions[2]) == self.__after_size:
                    interpolated = self.__interpolate([pair for partition in partitions for pair in partition])
                    for pair in interpolated[len(partitions[0]):len(interpolated)]:
                        yield pair
                    self.__ring.clear()
                    self.__ring.add_all(partitions[2])
                elif len(partitions[2]) < self.__after_size:
                    pass #We wait...
                else:
                    raise AssertionError()# We should not be here because of the ring size
            else: # we waited too much for something
                yield from partitions[0] + partitions[1]
                self.__ring.clear()
                self.__ring.add_all(partitions[2])
        elif len(partitions) == 2:
            if all_not_none(partitions[0]) and all_none(partitions[1]):
                if len(partitions[1]) > self.__interpolatable_size: 
                    # We give up :(
                    yield from partitions[1]
                    self.__ring.clear()
                else:
                    pass # Continue, dude! 
            elif all_none(partitions[0]) and all_not_none(partitions[1]):
                yield from partitions[0]
                self.__ring.clear()
                for pair in partitions[1]:
                    self.__ring.add(pair)
            else:
                raise AssertionError()# We should not be here... I guess. 
        elif len(self.__partitions) == 1:
            partition = self.__ring.partitions[0]
            if self.__are_items_absent(partition): # We're fucked anyway.
                yield from partition
                self.__ring.clear()
            else:
                if not self.__is_item_absent(appened_item):
                    yield appened_item
        else:
            raise AssertionError
    
    def __call__(self, iterator):
        for item in iterator:
            maybe = self.__ring.append(item)
            yield from self.__iterate(item, maybe)


