#!/bin/env python

from preggy import expect
from interpol import Something, Nothing, Left, Right


class TestEither(object):

    def test_something(self):
        something = Something(1)
        expect(something.is_something()).to_equal(True)
        expect(something.is_nothing()).to_equal(False)
        expect(something.value).to_equal(1)

    def test_nothing(self):
        nothing = Nothing()
        expect(nothing.is_something()).to_equal(False)
        expect(nothing.is_nothing()).to_equal(True)
        with expect.error_to_happen(ValueError):
            expect(nothing.value)

    def test_left(self):
        left = Left(1)
        expect(left.is_left()).to_equal(True)
        expect(left.is_right()).to_equal(False)
        expect(left.value).to_equal(1)
    
    def test_right(self):
        right = Right(1)
        expect(right.is_left()).to_equal(False)
        expect(right.is_right()).to_equal(True)
        expect(right.value).to_equal(1)


