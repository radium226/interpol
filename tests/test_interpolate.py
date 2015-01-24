#!/bin/env python

from nose.tools import assert_equals
from ..interpolate import Interpolate

import random
random.seed()

def assert_iterator_equals(left, right):
    left_list = list(left)
    right_list = list(right)
    assert len(left_list) == len(right_list)
    assert all(map(lambda pair: pair[0] == pair[1], zip(left_list, right_list)))

def list_enumerate(*l):
    return list(enumerate(l))

def probabilistic_random(*pairs):
    assert sum(map(lambda pair: pair[1], pairs)) == 1
    thresholds = []
    start = 0
    for value, probability in pairs:
        end = start + probability
        threshold = {"probability_start": start, "probability_end": end, "value": value}
        thresholds.append(threshold)
        start = end
    r = random.random()
    return list(map(lambda t: t["value"], filter(lambda t: t["probability_start"] <= r < t["probability_end"], thresholds)))[0]
    
def random_sample(size=50, min=-10, max=10):
    return list(enumerate(map(lambda v: v if probabilistic_random([False, 0.25], [True, 0.75]) else None, [random.randint(min, max + 1) for i in range(0, size)])))


class TestInterpolate(object):

    # Assert that no exception is raised when interpolating
    def assert_exception_not_raised(self, sample):
        try:
            interpolated_sample = self.interpolate(sample)
        except:
            #raise
            assert False
    
    def assert_interpolation_identity(self, sample):
        assert_iterator_equals(self.interpolate(sample), sample)
            
    # We recreate a new Interpolate object each time
    def setup(self):
        self.interpolate = Interpolate(1, 5, 1)
    
    # Test that no exception is raised
    def test_exception_not_raised(self):
        for sample in [random_sample() for _ in range(0, 100)]:
            yield self.assert_exception_not_raised, sample
    
    # Test interpolation on only one partition
    def test_interpolate_one_partition(self):
        samples = [
                list(range(1, 100)), 
                list(range(1, 2)), 
                [None] * 100, 
                [None] * 2
            ]
        for sample in map(lambda sample: list(enumerate(sample)), samples):
            yield self.assert_interpolation_identity, sample

    def test_interpolate_two_partitions_1(self):
        assert_iterator_equals(
                self.interpolate(list_enumerate(None, 2)), 
                list_enumerate(None, 2)
            )
    def test_interpolate_two_partitions_2(self):
        assert_iterator_equals(
                self.interpolate(enumerate([None] * 10 + [11])), 
                enumerate([None] * 10 + [11])
            )

    def test_interpolate_three_partitions_1(self):
        assert_iterator_equals(
                self.interpolate(list_enumerate(1, None, 3)), 
                list_enumerate(1, 2, 3)
            )
    
    def test_interpolate_three_partitions_2(self):
        assert_iterator_equals(
                self.interpolate(list_enumerate(None, 2, None)), 
                list_enumerate(None, 2, None)
            )
