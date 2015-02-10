#!/bin/env python

from interpol import PartitionedRing
from preggy import expect

def none_or_not_none(left, right):
    return left is None and right is not None or left is not None and right is None

class TestPartitionedRing(object):

    def test_append_one_partition(self):
        ring = PartitionedRing(partitions=3, items=10, boundary=none_or_not_none)
        ring.append(1)
        ring.append(2)
        expect(list(ring)).to_equal([1, 2])
        expect(len(ring.partitions)).to_equal(1)

    def test_append_two_partitions(self):
        ring = PartitionedRing(partitions=3, items=10, boundary=none_or_not_none)
        ring.append(1)
        ring.append(None)
        expect(list(ring)).to_equal([1, None])
        expect(len(ring.partitions)).to_equal(2)

    def test_append_more_than_three_partitions(self):
        ring = PartitionedRing(partitions=3, items=10, boundary=none_or_not_none)
        ring.append(1)
        ring.append(None)
        ring.append(3)
        ring.append(None)
        ring.append(5)
        expect(list(ring)).to_equal([3, None, 5])
        expect(len(ring.partitions)).to_equal(3)

    def test_too_much_append(self):
        ring = PartitionedRing(partitions=2, items=2, boundary=none_or_not_none)
        ring.append(1)
        ring.append(2)
        ring.append(3)
        expect(list(ring)).to_equal([2, 3])
        expect(len(ring.partitions)).to_equal(1)

    def test_too_much_append_at_the_end_of_a_partition(self):
        ring = PartitionedRing(partitions=2, items=2, boundary=none_or_not_none)
        ring.append(1)
        ring.append(None)
        ring.append(3)
        ring.append(4)
        ring.append(5)
        expect(list(ring)).to_equal([4, 5])
        expect(len(ring.partitions)).to_equal(1)

    def test_remove_partition(self):
        ring = PartitionedRing(partitions=2, items=2, boundary=none_or_not_none)
        ring.append(1)
        ring.append(None)
        ring.append(2)
        ring.remove_partition(0)
        expect(list(ring)).to_equal([2])
        expect(len(ring.partitions)).to_equal(1)


