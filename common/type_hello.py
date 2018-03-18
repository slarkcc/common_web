# -*- coding: utf-8 -*-
# @Time    : 2018/3/12 14:42
# @author  : slark
# @File    : type_hello.py
# @Software: PyCharm

import time, logging
from functools import wraps, partial


# 在函数上添加包装器
def time_this(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        print(end - start)
        return r

    return inner


# 解除一个装饰器
@time_this
def add(x, y):
    return x + y


orig_add = add.__wrapped__


# 定义一个带参数的装饰器
def logged(level, name=None, message=None):
    def decorate(func):
        log_name = name if name else func.__module__
        log = logging.getLogger(log_name)
        log_msg = message if message else func.__name__

        @wraps(func)
        def inner(*args, **kwargs):
            log.log(level, log_msg)
            return func(*args, **kwargs)

        return inner

    return decorate


@logged(logging.DEBUG)
def add(x, y):
    return x + y


# 定义可以自定义属性的装饰器

def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func


def logged(level, name=None, message=None):
    def decorate(func):
        log_name = name if name else func.__module__
        log = logging.getLogger(log_name)
        log_msg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, log_msg)
            return func(*args, **kwargs)

        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel

        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal log_msg
            log_msg = newmsg

        return wrapper

    return decorate


# 带可选参数的装饰器(可以带参数，或者不带)

def logged(func=None, *, level=logging.DEBUG, name=None, message=None):
    if func is None:
        return partial(logged, level=level, name=None, message=None)

    log_name = name if name else func.__module__
    log = logging.getLogger(log_name)
    log_msg = message if message else func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        log.log(level, log_msg)
        return func(*args, **kwargs)

    return wrapper


# 利用装饰器进行函数上的类型检查

from inspect import signature


def type_assert(*ty_args, **ty_kwargs):
    def decorate(func):
        if not __debug__:
            return func

        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)

            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            "Argument {} must be {}".format(name, bound_types[name])
                        )
            return func(*args, **kwargs)
        return wrapper

    return decorate
