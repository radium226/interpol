#!/bin/env python

from collections import deque as Deque
from enum import Enum
from itertools import tee
from .either import Left, Right, Nothing, Something

class PartitionedRing(object):

    def __init__(self, max_partition_count=None, max_item_count=None, boundary_matcher=None):
        self.__max_partition_count = max_partition_count
        self.__partitions = Deque(maxlen=max_partition_count)
        self.__is_item_boundary = boundary_matcher
        self.__max_item_count = max_item_count
    
    def __iter__(self):
        for partition in self.__partitions:
            yield from partition

    def last_appened():
        return self.__partitions[-1][-1]
    
    def append_all(self, items):
        for item in items:
            self.append(item)
    
    def append(self, item):
        maybe = Nothing()
        if len(self.__partitions) == 0:
            self.__partitions.append([item])
        else:
            last_partition = self.__partitions[-1]
            last_item = last_partition[-1]
            if self.__is_item_boundary(last_item, item):
                if len(self.__partitions) == self.__max_partition_count:
                    maybe = Something(Right(self.__partitions[0]))
                self.__partitions.append([item])
            else:
                last_partition.append(item)
        
            if len(self) > self.__max_item_count:
                maybe = Something(Left(self.__partitions[0][0]))
                self.__partitions[0] = self.__partitions[0][1:]
            
            if len(self.__partitions[0]) == 0:
                self.__partitions.popleft()
                maybe = Something(Right([maybe.value.value]))
        
        return maybe

        # left = item
        # right = partition
        
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
        return removed_partition

    @property
    def partitions(self):
        return self.__partitions

