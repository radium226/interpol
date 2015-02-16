#!/bin/env python

from .iterators import pairwise, partition, enumerate_successively
from enum import Enum

class State(Enum):
    NO_PRESENT_ITEM_HAVE_BEEN_APPENDED_YET = 1
    APPENDING_PRESENT_ITEMS_BEFORE_ABSENT_ITEMS = 2
    APPENDING_PRESENT_ITEMS_AFTER_ABSENT_ITEMS = 3
    APPENDING_ABSENT_ITEMS = 4


class Context(Enum):
    INSIDE_LOOP = 1
    OUTSIDE_LOOP = 2


class Item(object):
    
    def __init__(self, value, missing_value_matcher=lambda value: value is None):
        self.__value = value
        self.__match_missing_value = missing_value_matcher
    
    @property
    def value(self):
        return self.__value
    
    def is_absent(self):
        return self.__match_missing_value(self.__value)
    
    def is_present(self):
        return not self.is_absent()
    
    def __repr__(self):
        return "Item{value=%(value)s, present=%(present)s}" % {"value": self.__value, "present": "True" if self.is_present() else "False"}


def linear_interpolator(y_left, y_middle, y_right):
    xy_left, xy_middle, xy_right = enumerate_successively(y_left, y_middle, y_right)
    xy_a = xy_left[0]
    xy_b = xy_right[-1]
    x_a, y_a = xy_a
    x_b, y_b = xy_b
    def f(x):
        return (x_b - x) / (x_b - x_a) * y_a + (x - x_a) / (x_b - x_a) * y_b
    return [y_left, [f(x) for x in map(lambda xy: xy[0], xy_middle)], y_right]


class Interpolate(object):
    
    def __init__(self, minimal_present_item_count, maximal_absent_item_count, absent_value_matcher=lambda value: value is None, absent_value_interpolator=linear_interpolator):
        self.__state = State.NO_PRESENT_ITEM_HAVE_BEEN_APPENDED_YET
        self.__items = []
        self.__minimal_present_item_count = minimal_present_item_count
        self.__maximal_absent_item_count = maximal_absent_item_count
        self.__absent_value_matcher = absent_value_matcher
        self.__absent_value_interpolator = absent_value_interpolator
    
    @property
    def state(self):
        return self.__state
    
    @property
    def items(self):
        return self.__items

    def __interpolate(self, previous_present_items, absent_items, following_present_items):
        def value(item):
            return item.value

        def item(value):
            return Item(value, self.__absent_value_matcher)
        
        return [list(map(item, values)) for values in self.__absent_value_interpolator(list(map(value, previous_present_items)), list(map(value, absent_items)), list(map(value, following_present_items)))]
            
    def __repr__(self):
        return "Interpolate{state=%(state)s, %(items)s}" % {"state": repr(self.state), "items": repr(self.items)}

    def append(self, item):
        self.__items.append(item)
    
    def __iterate(self, *args, **kwargs):
        print("state = " + str(self.__state))
        def boundary_matcher(left_item, right_item):
            return left_item.is_absent() and right_item.is_present() or left_item.is_present() and right_item.is_absent()
        context = kwargs["context"]
        if context is Context.INSIDE_LOOP:
            item = args[0]
            print(item)
            if self.__state is State.NO_PRESENT_ITEM_HAVE_BEEN_APPENDED_YET:
                if item.is_absent():
                    self.__state = State.NO_PRESENT_ITEM_HAVE_BEEN_APPENDED_YET # We can only yield them and continue
                    yield item
                else: # item.is_present():
                    self.__state = State.APPENDING_PRESENT_ITEMS_BEFORE_ABSENT_ITEMS
                    yield from self.__iterate(*args, **kwargs)
            elif self.__state is State.APPENDING_PRESENT_ITEMS_BEFORE_ABSENT_ITEMS: 
                if item.is_present():
                    self.__state = State.APPENDING_PRESENT_ITEMS_BEFORE_ABSENT_ITEMS
                    self.__items.append(item)
                    yield item
                elif item.is_absent():
                    self.__state = State.APPENDING_ABSENT_ITEMS
                    yield from self.__iterate(*args, **kwargs)
                else:
                    raise AssertionError
            elif self.__state is State.APPENDING_ABSENT_ITEMS:
                if item.is_present():
                    self.__state = State.APPENDING_PRESENT_ITEMS_AFTER_ABSENT_ITEMS
                    yield from self.__iterate(*args, **kwargs)
                elif item.is_absent():
                    self.__state = State.APPENDING_ABSENT_ITEMS
                    self.__items.append(item)
                    present_items_before, absent_items = partition(boundary_matcher, self.__items)
                    if len(absent_items) > self.__maximal_absent_item_count:
                        print(" ---> " + str(absent_items))
                        yield from absent_items
                        self.__items.clear()
                        self.__state = State.NO_PRESENT_ITEM_HAVE_BEEN_APPENDED_YET
                    elif len(absent_items) <= self.__maximal_absent_item_count:
                         self.__state = State.APPENDING_ABSENT_ITEMS
                    else:
                        raise AssertionError
                else:
                    raise AssertionError
            elif self.__state is State.APPENDING_PRESENT_ITEMS_AFTER_ABSENT_ITEMS:
                if item.is_present():
                    self.__items.append(item)
                    present_items_before, absent_items, present_items_after = list(partition(boundary_matcher, self.__items))
                    if len(present_items_after) == self.__minimal_present_item_count:
                        
                        _, interpolated_items, _ = self.__interpolate(present_items_before, absent_items, present_items_after)
                        yield from interpolated_items
                        yield from present_items_after
                        self.__items.clear()
                        self.__items.extend(present_items_after)
                        self.__state = State.APPENDING_PRESENT_ITEMS_BEFORE_ABSENT_ITEMS
                    elif len(present_items_after) < self.__minimal_present_item_count:
                        self.__state = State.APPENDING_PRESENT_ITEMS_AFTER_ABSENT_ITEMS
                    else:
                        raise AssertionError
                elif item.is_absent():
                    present_items_before, absent_items, present_items_after = list(partition(boundary_matcher, self.__items))
                    if len(present_items_after) < self.__minimal_present_item_count:
                        self.__state = State.NO_PRESENT_ITEM_HAVE_BEEN_APPENDED_YET
                        yield from absent_items + present_items_after
                        yield item
                        self.__items.clear()
                    elif len(present_items_after) == self.__minimal_present_item_count:
                        self.__state = State.APPENDING_ABSENT_ITEMS
                    else:
                        raise AssertionError
                else:
                    raise AssertionError
            else:
                raise AssertionError
        elif context is Context.OUTSIDE_LOOP:
            if self.__state is State.APPENDING_PRESENT_ITEMS_AFTER_ABSENT_ITEMS:
                present_items_before, absent_items, present_items_after = list(partition(boundary_matcher, self.__items))
                yield from absent_items + present_items_after
            elif self.__state is State.APPENDING_ABSENT_ITEMS:
                present_items_before, absent_items = list(partition(boundary_matcher, self.__items))
                yield from absent_items
            else:
                pass
        
    def __call__(self, iterator):
        for value in iterator:
            yield from map(lambda item: item.value, self.__iterate(Item(value), context=Context.INSIDE_LOOP))
        yield from map(lambda item: item.value, self.__iterate(context=Context.OUTSIDE_LOOP))

