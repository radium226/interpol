#!/bin/env python

from nose.tools import assert_equals
from interpolate import Interpolate

def assert_iterator_equals(left, right):
    assert len(list(left)) == len(list(right))
    assert all(map(lambda pair: pair[0] == pair[1], zip(left, right)))

def list_enumerate(*l):
    return list(enumerate(l))

class TestInterpolate(object):

    # We recreate the object each time
    @property
    def interpolate(self):
        return Interpolate(1, 5, 1)    

    def test_interpolate_one_partition(self):
        identities = [
                list(range(1, 100)), 
                list(range(1, 2)), 
                [None] * 100, 
                [None] * 2
            ]
        for identity in identities:
            assert_iterator_equals(
                    self.interpolate(enumerate(identity)), 
                    enumerate(identity)
                )

    def test_interpolate_two_partitions(self):
        assert_iterator_equals(
                self.interpolate(list_enumerate(None, 2)), 
                list_enumerate(None, 2)
            )

        assert_iterator_equals(
                self.interpolate(enumerate([None] * 10 + [11])), 
                enumerate([None] * 10 + [11])
            )

    def test_interpolate_three_partitions(self):
        assert_iterator_equals(
                self.interpolate(list_enumerate(1, None, 3)), 
                list_enumerate(1, 2, 3)
            )
        print(" --> " + repr(list(self.interpolate(list_enumerate(None, 2, None)))))
        assert_iterator_equals(
                self.interpolate(list_enumerate(None, 2, None)), 
                list_enumerate(None, 2, None)
            )
