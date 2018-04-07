# -*- coding: utf-8 -*-
# @Time    : 2018/4/7 下午1:00
# @author  : slark
# @File    : debug_hello.py
# @Software: PyCharm
import pdb
import logging

logging.basicConfig(level=logging.INFO)


def foo(c):
    m = int(c)
    assert m != 0, 'n is zero!'  # 一个判断条件，如果真则顺利执行下面的语句，如果为假则触发AssertionError异常
    return 10 / m


def main():
    foo('0')


# if __name__ == "__main__":
#     s = '0'
#     n = int(s)
#     logging.info('n = {}'.format(n))
#     print(10 / n)

s = '0'
n = int(s)
pdb.set_trace()  # 执行到这里暂停运行，输入p 变量名可以查看变量值，输入c可以继续执行
print(10 / n)
