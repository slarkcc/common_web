# -*- coding: utf-8 -*-
# @Time    : 2018/1/21 15:44
# @author  : slark
# @File    : decorator_.py
# @Software: PyCharm
from inspect import signature
import functools, time

# 检查函数的参数，如果参数不是整数，则报错
import logging


def decorator(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        kwargs_values = [value for value in kwargs.values()]
        for arg in list(args) + kwargs_values:
            if not isinstance(arg, int):
                raise TypeError("{0} only accept integers as arguments ".format(func.__name__))

        return func(*args, **kwargs)

    return inner


def time_this(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end - start)
        return result

    return inner


# 接受可选参数的装饰器
def logged(func=None, *, level=logging.DEBUG, name=None, message=None):
    if func is None:
        return functools.partial(logged, level=level, name=name, message=message)
    logname = name if name else func.__module__
    log = logging.getLogger(logname)
    logmsg = message if message else func.__name__

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        log.log(level, logmsg)
        return func(*args, **kwargs)

    return wrapper


@logged
def add1():
    return 1 + 2


# 相当于add1 = logged(add1)


@logged(level=logging.CRITICAL, name="example")
def add2():
    return 3 + 2


# 相当于add2 = logged(level=logging.CRITICAL, name="example")(add2)


#####################################################################
def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        if not __debug__:
            return func

        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            for name, value in bound_values.arguments.items():
                pass


# 在类中定义装饰器
class A(object):
    def decorator1(self, func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            print("decorator1")
            return func(*args, **kwargs)

        return inner

    @classmethod
    def decorator(cls, func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            print("decorator2")
            return func(*args, **kwargs)

        return inner
