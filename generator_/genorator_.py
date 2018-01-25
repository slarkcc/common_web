# -*- coding: utf-8 -*-
# @Time    : 2018/1/24 17:43
# @author  : slark
# @File    : genorator_.py
# @Software: PyCharm
import time


def fibonacci(num):
    result = list()
    for i in range(num):
        if i < 2:
            result.append(1)
        else:
            result.append(sum(result))
            result.pop(0)
        yield result[-1]


def squares(cur=1, num=100):
    """
    实现跳跃，跳跃后如果不再给send值，则从跳跃后的值继续开始
    :param cur:
    :param num:
    :return:
    """
    response = None

    while num > 0:
        response = yield cur ** 2

        if response:
            cur = int(response)
        else:
            cur += 1

        num -= 1


def squares1(cur=1, num=100):
    """
    实现跳跃的生成器，跳跃后如果不再给send值，则从端点处继续。
    :param cur:
    :param num:
    :return:
    """
    response = 0

    while num > 0:
        if response:
            response = yield response ** 2
        else:
            response = yield cur ** 2
            cur += 1
        num -= 1


# 用生成器实现消费/生产者模型
def consumer():
    r = 0
    while True:
        n = yield r
        if not n:
            raise StopIteration(n)
        else:
            print('[CONSUMER] Consuming %s...' % n)
            time.sleep(1)
            r = '200 ok'


def produce(c):
    c.next()
    n = 0
    while n < 5:
        n += 1
        print ('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print ('[PRODUCER] Consumer return: %s' % r)
    c.close()
