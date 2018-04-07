# -*- coding: utf-8 -*-
# @Time    : 2018/1/27 17:43
# @author  : slark
# @File    : any_things.py
# @Software: PyCharm
import heapq


# 优先级队列
class PriorityQueue(object):
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]


class Item:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Item({!r})".format(self.name)


#  查找序列中的最大或者最小的n个元素
#   1 先排序，然后切片
#   2 使用堆排序
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print(heapq.nlargest(3, nums))  # Prints [42, 37, 23]
print(heapq.nsmallest(3, nums))  # Prints [-4, 1, 2]
portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
    {'name': 'FB', 'shares': 200, 'price': 21.09},
    {'name': 'HPQ', 'shares': 35, 'price': 31.75},
    {'name': 'YHOO', 'shares': 45, 'price': 16.35},
    {'name': 'ACME', 'shares': 75, 'price': 115.65}
]
cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])


def bin_search(data_list, val):
    low = 0
    high = len(data_list) - 1

    while low <= high:
        mid = (low + high) // 2
        if data_list[mid] == val:
            return mid
        elif data_list[mid] > val:
            high = mid - 1
        else:
            low = mid + 1

    return "Not exist !!"


import functools


# 装饰器实现
def singleton(cls):
    instance = {}

    @functools.wraps(cls)
    def getinstance(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return getinstance


# 使用元类
class Singleton(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


# 使用__new__
class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


def singleton(cls):
    instance = {}

    @functools.wraps(cls)
    def inner(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return inner


# 冒泡排序算法
def bubble_sort(nums):
    for i in range(len(nums) - 1):
        for j in range(len(nums) - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums


# 二分查找算法
def binary_search(li, val):
    low = 0
    high = len(li) - 1

    while low < high:
        mid = (low + high) // 2
        if val == li[mid]:
            return mid
        elif val < li[mid]:
            high = mid - 1
        else:
            low = mid + 1

    return "Don't exist !!"



