#!/bin/env python

from itertools import tee

def enumerate_successively(*lists):
    index = 0
    enumerated_lists = []
    for l in lists:
        enumerated_lists.append(list(enumerate(l, start=index)))
        index += len(l)
    return enumerated_lists
   

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def partition(boundary_matcher, iterator):
    if boundary_matcher is None:
        yield list(iterator)
    else:
        partition = []
        for index, left_and_right_items in enumerate(pairwise(iterator)):
            left_item, right_item = left_and_right_items
            # Deal with first partition
            if index == 0:
                partition.append(left_item)
            if boundary_matcher(left_item, right_item):
                yield partition
                partition = []
            partition.append(right_item)
        
        # Deal with last partition
        if partition:
            yield partition 
