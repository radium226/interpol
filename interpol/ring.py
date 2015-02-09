#!/bin/env python

from collections import deque as Deque
from enum import Enum
from itertools import tee

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def partition(iterator, boundary_matcher):
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
            
class PartitionedRing(object):

    def __init__(self, partitions=None, items=None, boundary=None):
        self.__partitions = Deque(maxlen=partitions)
        self.__boundary = boundary
        self.__max_length = items
    
    def __iter__(self):
        for partition in self.__partitions:
            yield from partition
    
    def append(self, item):
        removed_partition = None
        removed_item = None
        if len(self.__partitions) == 0:
            self.__partitions.append([item])
        else:
            last_partition = self.__partitions[-1]
            last_item = last_partition[-1]
            if self.__boundary(last_item, item):
                self.__partitions.append([item])
            else:
                last_partition.append(item)
        
            if len(self) > self.__max_length:
                removed_item = self.__partitions[0][0]
                self.__partitions[0] = self.__partitions[0][1:]
            
            if len(self.__partitions[0]) == 0:
                removed_partiton = self.__partitions.popleft()
        
        return removed_partition if removed_partition is not None else removed_item if removed_item is not None else None
        
    def __len__(self):
        return sum(map(lambda partition: len(partition), self.__partitions))
        
    def __repr__(self):
        return repr(list(self.__partitions))
    
    def remove_partition(self, partition_index):
        partitions = list(self.__partitions)
        removed_partition = None
        self.__partitions.clear()
        for index, partition in enumerate(partitions):
            if index != partition_index:
                self.__partitions.append(partition)
            else:
                removed_partition = partition
        return partition

    @property
    def partitions(self):
        return self.__partitions

if __name__ == "__main__":
    def append_to_ring(ring, item):
        i = ring.append(item)
        print(repr(ring) + " <---> " + repr(i))
        return i
    
    ring = PartitionedRing(items=5, partitions=2, boundary=lambda r, l: r is None and l is not None or r is not None and l is None)
    append_to_ring(ring, 1)
    append_to_ring(ring, 2)
    append_to_ring(ring, 3)
    append_to_ring(ring, 4)
    append_to_ring(ring, 5)
    append_to_ring(ring, None)
    append_to_ring(ring, None)
    append_to_ring(ring, None)
    append_to_ring(ring, None)
    append_to_ring(ring, None)
    append_to_ring(ring, 12)
    
    ring.remove_partition(1)
    print(ring)
