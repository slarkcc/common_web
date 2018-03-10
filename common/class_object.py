# -*- coding: utf-8 -*-
# @Time    : 2018/2/8 13:55
# @author  : slark
# @File    : class_object.py
# @Software: PyCharm
from functools import partial
import math


# 创建大量对象时节省内存
class Date(object):
    __slots__ = ["year", "month", "day"]  # 使用slots后，不能再给实例添加新属性

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day


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


# 改变对象的字符串显示
class Pair(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):  # __repr__() 方法返回一个实例的代码表示形式，通常用来重新构造这个实例。 内置的 repr() 函数返回这个字符串，跟我们使用交互式解释器显示的值是一样的
        return "Pair {0.x!r}, {0.y!r}".format(self)  # !r 格式化代码指明输出使用 __repr__() 来代替默认的 __str__()

    def __str__(self):  # __str__() 方法将实例转换为一个字符串，使用 str() 或 print() 函数会输出这个字符串,如果str没有定义就会被repr代替
        return "{0.x!s}, {0.y!s}".format(self)


# 自定义字符串的格式化
_formats = {
    'ymd': '{d.year}-{d.month}-{d.day}',
    'mdy': '{d.month}/{d.day}/{d.year}',
    'dmy': '{d.day}/{d.month}/{d.year}',
}


class Date(object):
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, format_spec):
        if format_spec == '':
            format_spec = 'ymd'
        fmt = _formats[format_spec]
        return fmt.format(d=self)


# 让对象支持上下文管理协议
from socket import socket, AF_INET, SOCK_STREAM


class LazyConnection(object):
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.type = type
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError("Already connected")
        self.sock = socket(self.family, self.type)
        self.sock.connect(self.address)

        return self.sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()
        self.sock = None


class LazyConnection1(object):
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.type = type
        self.connections = []

    def __enter__(self):
        sock = socket(self.family, self.type)
        sock.connect(self.address)
        self.connections.append(sock)
        return sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connections.pop().close()


from functools import partial

conn1 = LazyConnection1(('www.python.org', 80))
with conn1 as s1:
    pass
    with conn1 as s2:
        pass

conn = LazyConnection(('www.python.org', 80))

with conn as s:
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))


# 创建大量对象时节省内存方法
class Date(object):
    __slots__ = ['year', 'month', 'day']

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day


# 在类中封装属性名
class A(object):
    def __init__(self):
        self._internal = 0
        self._public = 1

    def public_method(self):
        pass

    def _internal_method(self):
        pass


class B(object):
    def __init__(self):
        self.__private = 0  # 变成_B__private

    def __private_method(self):  # 变成_B__private_method
        pass

    def public_method(self):
        pass


class C(B):
    def __init__(self):
        super().__init__()  # python3中可以直接super().method()但在python2中super(C, self).method()
        self.__private = 1  # 不能覆盖父类的属性

    def __private_method(self):
        print("hell")


# super()用法,super()根据传进去的两个参数：
#    通过第一参数传进去的类名确定当前在MRO中的哪个位置。MRO(Method Resolution Order)
#    通过第二个参数传进去的self，确定当前的MRO列表
# def super(cls, inst):
#     mro = inst.__class__.mro() #确定当前MRO列表
#     return mro[mro.index(cls) + 1] #返回下一个类

# MRO列表遵循的三条准则（C3 算法）：
#       子类会先于父类被检查
#       多个父类会根据它们在列表中的顺序被检查
#       如果对下一个类存在两个合法的选择，选择第一个父类
class A(object):
    def name(self):
        print('from A')
        super(A, self).name()


class B(object):
    def name(self):
        print('from B')


class C(A, B):
    def name(self):
        print('from C')
        super(C, self).name()


# 创建可管理的属性
class Person(object):
    def __init__(self, first_name):
        self.first_name = first_name

    @property
    def first_name(self):  # 必须先定义first_name属性
        return self._first_name  # 数据实际保存的地方

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Expected a string")
        self._first_name = value

    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")


class Person(object):
    def __init__(self, first_name):
        self.first_name = first_name

    def get_first_name(self):
        return self.first_name

    def set_first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Expected a string")
        self.first_name = value

    def del_first_name(self):
        raise AttributeError("Can't delete attribute")

    name = property(get_first_name, set_first_name, del_first_name)


# 调用父类方法
class A(object):
    def spam(self):
        print("A: spam")


class B(A):
    def spam(self):
        print("B: spam")
        super(B, self).spam()


class A(object):
    def __init__(self):
        self.x = 0


class B(A):
    def __init__(self):
        super(B, self).__init__()
        self.y = 1


class Proxy(object):
    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, item):
        return getattr(self.obj, item)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            super(Proxy, self).__setattr__(key, value)
        else:
            setattr(self.obj, key, value)


# 子类中扩展property
class Person(object):
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


# 重写父类的name属性
class SubPerson(Person):
    @property
    def name(self):
        print('Getting name')
        return super().name

    @name.setter
    def name(self, value):
        print('Setting name to')
        super(SubPerson, SubPerson).name.__set__(self, value)

    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)


# 只重写某个方法
class SubPerson(object):
    @Person.name.getter
    def name(self):
        print("Getting name")
        return super().name


class SubPerson(Person):
    @Person.name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)


# 创建新的类或实例属性
class Integer(object):
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError("Expected int")
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class Point(object):
    x = Integer('x')
    y = Integer('y')

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Typed(object):
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('Expected' + str(self.expected_type))
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


def typeassert(**kwargs):
    def decorate(cls):
        for name, expected_type in kwargs.items():
            setattr(cls, name, Typed(name, expected_type))
        return cls

    return decorate


@typeassert(name=str, shares=int, price=float)
class Stock(object):
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


# 使用延迟计算属性
class Lazyproperty(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


import math


class Circle(object):
    def __init__(self, radius):
        self.radius = radius

    @Lazyproperty
    def area(self):
        print("Computing area")
        return math.pi * self.radius * 2

    @Lazyproperty
    def perimeter(self):
        print("Computing perimeter")
        return 2 * math.pi * self.radius


# 简化数据结构的初始化
import math


class Structure1(object):
    _fields = []

    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError("Expected {} arguments".format(len(self._fields)))

        for name, value in zip(self._fields, args):
            setattr(self, name, value)


class Stock(Structure1):
    _fields = ['name', 'shares', 'price']


class Point(Structure1):
    _fields = ['x', 'y']


class Circle(Structure1):
    _fields = ['radius']

    def area(self):
        return math.pi * self.radius ** 2


class Structure2(object):
    _fields = []

    def __init__(self, *args, **kwargs):
        if len(args) > len(self._fields):
            raise TypeError("Expected {} arguments".format(len(self._fields)))

        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        for name in self._fields[len(args):]:
            setattr(self, name, kwargs.pop(name))

        if kwargs:
            raise TypeError("Invalid argument(s):".format(','.join(kwargs)))


class Structure3(object):
    _fields = []

    def __init__(self, *args, **kwargs):
        if len(args) != len(self._fields):
            raise TypeError("Expected {} arguments".format(len(self._fields)))

        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        extra_args = kwargs.keys() - self._fields

        for name in extra_args:
            setattr(self, name, kwargs.pop(name))

        if kwargs:
            raise TypeError("Duplicate values for {}".format(','.join(kwargs)))


# 定义接口或者抽象基类
from abc import ABCMeta, abstractmethod


class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxbytes=-1):
        pass

    @abstractmethod
    def write(self, data):
        pass


def serialize(obj, stream):
    if not isinstance(stream, IStream):
        raise TypeError("Expected an IStream")
    pass


import io

IStream.regester(io.IOBase)

f = open('foo.txt')
isinstance(f, IStream)


# 实现数据模型的类型约束
class Descriptor(object):
    def __init__(self, name=None, **opts):
        self.name = name
        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        instance.__dict__[self.nane] = value


class Typed(Descriptor):
    expected_type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise ValueError("expected" + str(self.expected_type))
        super(Typed, self).__set__(instance, value)


class Unsigned(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Expected >= 0")
        super().__set__(instance, value)


class MaxSized(Descriptor):
    def __init__(self, name=None, **opts):
        if 'size' not in opts:
            raise TypeError("missing size option")

        super(MaxSized, self).__init__(name, **opts)

    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError('size must be <' + str(self.size))

        super(MaxSized, self).__set__(instance, value)


# 使用类装饰器
def check_attribute(**kwargs):
    def decorator(cls):
        for key, value in kwargs.items():
            if isinstance(value, Descriptor):
                value.name = key
                setattr(cls, key, value)
            else:
                setattr(cls, key, value(key))
        return cls

    return decorator


@check_attribute(name=SizedString(size=8),
                 shares=UnsignedInteger,
                 price=UnsignedFloat)
class Stock(object):
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


# 使用元类实现
class checkedmeta(type):
    def __new__(cls, clsname, bases, methods):
        for key, value in methods.items():
            if isinstance(value, Descriptor):
                value.name = key
            return type.__new__(cls, clsname, bases, methods)


# 实现自定义容器

import collections
import bisect


class A(collections.Iterable):
    pass


class SortedItems(collections.Sequence):
    def __init__(self, initial=None):
        self._items = sorted(initial) if initial is not None else []

    def __getitem__(self, item):
        return self._items[item]

    def __len__(self):
        return len(self._items)

    def __add__(self, other):
        bisect.insort(self._items, other)


# 属性的代理访问
class A(object):
    def spam(self, x):
        pass

    def foo(self):
        pass


class B1(object):
    def __init__(self):
        self._a = A()

    def spam(self, x):
        return self._a.spam(x)

    def foo(self):
        return self._a.foo()

    def bar(self):
        pass


# 当有大量方法时
class B2(object):
    def __init__(self):
        self._a = A()

    def bar(self):
        pass

    def __getattr__(self, item):
        return getattr(self._a, item)


# 实现代理模式
class Proxy(object):
    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, item):
        print("getattr:", item)
        return getattr(self._obj, item)

    def __setattr__(self, key, value):
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            print("setattr:", key, value)
            setattr(self._obj, key, value)

    def __delattr__(self, item):
        if item.startswith("_"):
            super().__delattr__(item)
        else:
            print("delattr:", item)
            delattr(self._obj, item)


class Spam(object):
    def __init__(self, x):
        self.x = x

    def bar(self, y):
        print('spam.bar:', self.x, y)


s = Spam(3)

p = Proxy(s)

print(p.x)
p.bar()
p.x = 37

# 在类中定义多个构造器
import time


class Date(object):
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)


# 创建不调用init方法的实例
class Date(object):
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day


d = Date.__new__(Date)  # 绕过__init__方法，这样d是没有year， month， day属性的
d.year  # 报错

from time import localtime


class Date(object):
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def today(cls):
        d = cls.__new__(cls)
        t = localtime()
        d.year = t.tm_mday
        d.month = t.tm_mon
        d.day = t.tm_mday
        return d


# 利用Mixins扩展功能

class LoggedMappingMixin(object):
    __slots__ = ()

    def __getitem__(self, item):
        print("Getting " + str(item))
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        print("Setting {} = {!r}".format(key, value))
        return super().__setitem__(key, value)

    def __delitem__(self, key):
        print("Deleting " + str(key))
        return super().__delitem__(key)


class SetOnceMappingMixin(object):
    __slots__ = ()

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(str(key) + "already set")
        return super().__setitem__(key, value)


class StringKeyMappingMixin(object):
    __slots__ = ()

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError('key must be strings')
        return super().__setitem__(key, value)


class LoggedDict(LoggedMappingMixin, dict):
    pass


# 实现状态对象或者状态机

class Connection(object):

    def __init__(self):
        self.state = "CLOSED"

    def read(self):
        if self.state != "OPEN":
            raise RuntimeError('Not open')
        print('reading')

    def write(self, data):
        if self.state != "OPEN":
            raise RuntimeError("Not open")
        print("writing")

    def open(self):
        if self.state == "OPEN":
            raise RuntimeError("Already open")
        self.state = "OPEN"

    def close(self):
        if self.state == "CLOSED":
            raise RuntimeError("Already closed")
        self.state = "CLOSED"


class Connection1(object):

    def __init__(self):
        self.new_state(ClosedConnectionState)

    def new_state(self, newstate):
        self._state = newstate

    def read(self):
        return self._state.read(self)

    def write(self, data):
        return self._state.write(self, data)

    def open(self):
        return self._state.open(self)

    def close(self):
        return self._state.close(self)


class ConnectionState(object):
    @staticmethod
    def read(conn):
        raise NotImplementedError()

    @staticmethod
    def write(conn):
        raise NotImplementedError()

    @staticmethod
    def open():
        raise NotImplementedError()

    @staticmethod
    def close():
        raise NotImplementedError()


class ClosedConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        raise RuntimeError('Not open')

    @staticmethod
    def write(conn):
        raise RuntimeError("Not open")

    @staticmethod
    def open(conn):
        conn.new_state(OpenConnectionState)

    @staticmethod
    def close(conn):
        raise RuntimeError('Already closed')


class OpenConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        print('reading')

    @staticmethod
    def write(conn, data):
        print('writing')

    @staticmethod
    def open(conn):
        raise RuntimeError('Already open')

    @staticmethod
    def close(conn):
        conn.new_state(ClosedConnectionState)


# 通过字符串调用对象方法

import math


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point({!r:},{!r:})'.format(self.x, self.y)

    def distance(self, x, y):
        return math.hypot(self.x - x, self.y - y)


p = Point(2, 3)

d = getattr(p, 'distance')(0, 0)

import operator

operator.methodcaller('distance', 0, 0)(p)


# 实现访问者模式

class Node(object):
    pass


class UnaryOperator(Node):

    def __init__(self, operand):
        self.operand = operand


class BinaryOperator(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class Add(BinaryOperator):
    pass


class Sub(BinaryOperator):
    pass


class Mul(BinaryOperator):
    pass


class Div(BinaryOperator):
    pass


class Negate(UnaryOperator):
    pass


class Number(Node):

    def __init__(self, value):
        self.value = value


class NodeVisitor(object):

    def visit(self, node):
        methname = 'visit_' + type(node).__name__
        meth = getattr(self, methname, None)
        if meth is None:
            meth = self.generic_visit
        return meth(node)

    def generic_visit(self, node):
        raise RuntimeError("No {} method".format('visit_' + type(node).__name__))


class Evaluator(NodeVisitor):
    def visit_number(self, node):
        return node.value

    def visit_Add(self, node):
        return self.visit(node.left) + self.visit(node.right)

    def visit_Sub(self, node):
        return self.visit(node)
