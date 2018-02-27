# -*- coding: utf-8 -*-
# @Time    : 2018/2/8 13:55
# @author  : slark
# @File    : class_object.py
# @Software: PyCharm
from socket import socket, AF_INET, SOCK_STREAM
from functools import partial
import math


class Pair(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):  # 使用实例名时调用
        return "Pair ({0.x!r}, {0.y!r})".format(self)  # ! 指定用__repr__方法

    def __str__(self):  # 使用print时调用，没有定义时访问__repr__
        return '({0.x!s}, {0.y!s})'.format(self)  # !s指定用__str__方法


# 自定义字符串格式化
class Date(object):
    _formats = {
        'ymd': '{d.year}-{d.month}-{d.day}',
        'mdy': '{d.month}-{d.day}-{d.year}',
        'dmy': '{d.day}-{d.month}-{d.year}',
    }

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, format_spec):
        if format_spec == '':
            format_spec = 'ymd'
        fmt = self._formats[format_spec]
        return fmt.format(d=self)


# 上下文管理器
class LazyConnection(object):
    def __init__(self, address, family=AF_INET, type_=SOCK_STREAM):
        self.address = address
        self.family = family
        self.type_ = type_
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            self.sock = socket(self.family, self.type_)
            self.sock.connect(self.address)
            return self.sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()
        self.sock = None


class LazyConnection1(object):
    def __init__(self, address, family=AF_INET, type_=SOCK_STREAM):
        self.address = address
        self.family = family
        self.type_ = type_
        self.connections = []

    def __enter__(self):
        sock = socket(self.family, self.type_)
        sock.connect(self.address)
        self.connections.append(sock)
        return sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connections.pop().close()


conn = LazyConnection1(('www.python.org', 80))
with conn as s1:
    pass
    with conn as s2:
        pass


# 创建大量对象时节省内存
class Date(object):
    __slots__ = ["year", "month", "day"]  # 使用slots后，不能再给实例添加新属性

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day


# 在类中封装属性名,使用单下划线表示私有变量，仅在内部使用
class A(object):
    def __init__(self):
        self._internal = 0
        self.public = 1

    def public_method(self):
        pass

    def _internal_method(self):
        pass


# 使用双下划线时，外部无法通过该名字访问
class B(object):
    def __init__(self):
        self.__private = 0

    def __private_method(self):
        pass

    def public_method(self):
        pass
        self.__private_method()


class C(B):
    def __init__(self):
        super(C, self).__init__()
        self.__private = 1  # 将不会重写B中的__private

    def __private_method(self):  # 将不会重写B中的__private_method
        pass


# 创建可管理的属性
class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    # Getter function
    @property
    def first_name(self):
        return self._first_name

    # Setter function
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # Deleter function (optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")


class Person1(object):
    def __init__(self, first_name):
        self.set_first_name(first_name)

    def get_first_name(self):
        return self._first_name

    def set_first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Expected a string")
        self._first_name = value

    def del_first_name(self):
        raise AttributeError("Can't delete attribute")

    name = property(get_first_name, set_first_name, del_first_name)


class Circle(object):

    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return math.pi * self.radius ** 2

    @property
    def diameter(self):
        return self.radius * 2

    @property
    def perimeter(self):
        return 2 * math.pi * self.radius


# 调用父类方法
class A1(object):
    def spam(self):
        print('A.spam')


class B1(A1):
    def spam(self):
        print('B.spam')
        super(B1, self).spam()


class A2(object):
    def __init__(self):
        self.x = 0


class B2(A2):
    def __init__(self):
        super(B2, self).__init__()  # 用来保障父类的初始化被正确执行
        self.y = 1


class Proxy(object):
    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, item):
        return getattr(self._obj, item)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            super(Proxy, self).__setattr__(key, value)
        else:
            setattr(self._obj, key, value)


# 在子类中扩展property
class Person2(object):
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Expected a string")
        self._name = value

    @name.deleter
    def name(self):
        raise AttributeError("Can't delete attribute")


class SubPerson(Person2):
    @property
    def name(self):
        print("Getting name")
        return super(SubPerson, self).name

    @name.setter
    def name(self, value):
        print('Setting name to', value)
        super(Person2, self).name.__set__(self, value)

    @name.deleter
    def name(self):
        print("Deleting name")
        super(Person2, self).name.__delete__(self)


# 创建新的类或实例属性
class Integer(object):
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError("Expected an int")
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

# 数据描述符
