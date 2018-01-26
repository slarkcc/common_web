# -*- coding: utf-8 -*-
# @Time    : 2018/1/21 15:44
# @author  : slark
# @File    : decorator_.py
# @Software: PyCharm

import functools


# 检查函数的参数，如果参数不是整数，则报错
def decorator(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        kwargs_values = [value for value in kwargs.values()]
        for arg in list(args) + kwargs_values:
            if not isinstance(arg, int):
                raise TypeError("{0} only accept integers as arguments ".format(func.__name__))

        return func(*args, **kwargs)

    return inner
