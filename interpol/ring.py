#!/bin/env python

from collections import deque as Deque
from enum import Enum
from itertools import tee

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

