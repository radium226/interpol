#!/bin/env python

from nose.tools import assert_equals
from interpol import Interpolate, linear_interpolator, enumerate_successively
from preggy import expect, create_assertions
from itertools import tee, zip_longest
import random

@create_assertions
def to_amount(topic, expected, comparator=lambda a, b: a == b):
    return all(comparator(a, b) for a, b in zip_longest(topic, expected, fillvalue=object()))

random.seed()

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

    # We first test the
    def test_enumerate_successively(self):
        expect((enumerate_successively([0], [1, 2], [3]))).to_amount([[(0, 0)], [(1, 1), (2, 2)], [(3, 3)]])

    def test_linear_interpolator(self):
        expect(linear_interpolator([1], [None, None, None], [5])).to_amount([[1], [2, 3, 4], [5]])

    def test_interpolate_1(self):
        interpolate = Interpolate(2, 3)
        expect(interpolate([1, 2, 3, None, None, None, 7, 8])).to_amount([1, 2, 3, 4, 5, 6, 7, 8])
    
    def test_interpolate_2(self):
        interpolate = Interpolate(2, 3)
        input =  [1, 2, None, None, 5, 6, 7, None, None, 10, None, None, None, None, 15, 16, 17, None, None, None, None]
        output = [1, 2,    3,    4, 5, 6, 7, None, None, 10, None, None, None, None, 15, 16, 17, None, None, None, None]
        expect([round(n) if n is not None else None for n in interpolate(input)]).to_equal(output)


    def test_interpolate_3(self):
        interpolate = Interpolate(2, 3)
        expect(interpolate([None, 1, 2, None, 4, 5, None, 7, 8, None, None, 11, 12, None])).to_amount([None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, None])
        

'''
    def test_interpolate_two_partitions_3(self):
        expect(
                Interpolate(2, 3)(enumerate([1] + [None] * 10 + [2, 3, 4, 5] + [None] * 5 + [6, 7, 8, 9])), 
                enumerate([1] + [None] * 10 + [2, 3, 4, 5]+ [None] * 5 + [6, 7, 8, 9])
            )
    
    def test_interpolate_two_partitions_4(self):
        assert_iterator_equals(
                Interpolate(2, 3)(enumerate([1, 2] + [None] * 10 + [3, 4, 5, 6])), 
                enumerate([1, 2] + [None] * 10 + [3, 4, 5, 6])
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
    
    def test_interpolate_three_partitions_3(self):
        assert_iterator_equals(
                self.interpolate(list_enumerate(1, 2, 3, 4, None, 6)), 
                list_enumerate(1, 2, 3, 4, 5, 6)
            )
    
    def test_interpolate_three_partitions_3(self):
        assert_iterator_equals(
                Interpolate(3, 3)(list_enumerate(1, 2, 3, None, None, None, 7, None, 8)), 
                list_enumerate(1, 2, 3, None, None, None, 7, None, 8)
            )
            
    def test_interpolate_three_partitions_4(self):
        assert_iterator_equals(
                Interpolate(2, 3)(enumerate([1, 2, None, None, 5, None, 7, 8, None, 10, 11, None])), 
                enumerate([1, 2, None, None, 5, None, 7, 8, 9, 10, 11, None])
            )
'''
