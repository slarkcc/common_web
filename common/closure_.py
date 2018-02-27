# -*- coding: utf-8 -*-
# @Time    : 2018/1/26 14:45
# @author  : slark
# @File    : closure_.py
# @Software: PyCharm


def count():
    result = []

    for i in range(3):
        def inner():
            return i ** 2

        result.append(inner)
    return result


def lazy_sum(n):
    def sum_():
        result = 0
        for i in range(n):
            result += i
        return result

    return sum_


