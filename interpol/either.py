#!/bin/env python

from abc import abstractmethod, ABCMeta


class Either(metaclass=ABCMeta):

    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @abstractmethod
    def is_left(self):
        raise NotImplementedError

    @abstractmethod
    def is_right(self):
        raise NotImplementedError


class Left(Either):

    def __init__(self, value):
        super().__init__(value)

    def is_right(self):
        return False

    def is_left(self):
        return True

    def __repr__(self):
        return "Left(%s)" % repr(self.value)


class Right(Either):

    def __init__(self, value):
        super().__init__(value)

    def is_right(self):
        return True

    def is_left(self):
        return False

    def __repr__(self):
        return "Right(%s)" % repr(self.value)


class Maybe(metaclass=ABCMeta):

    def __init__(self, value):
        self.__value = value

    @abstractmethod
    def is_nothing(self):
        raise NotImplementedError

    @abstractmethod
    def is_something(self):
        raise NotImplementedError

    @property
    def value(self):
        return self.__value


class Something(Maybe):

    def __init__(self, value):
        super().__init__(value)

    def is_something(self):
        return True

    def is_nothing(self):
        return False

    def __repr__(self):
        return "Something(%s)" % repr(self.value)


class Nothing(Maybe):

    def __init__(self):
        super().__init__(None)

    def is_something(self):
        return False

    def is_nothing(self):
        return True

    @property
    def value(self):
        raise ValueError("What the hell are you doing? ")

    def __repr__(self):
        return "Nothing()"
