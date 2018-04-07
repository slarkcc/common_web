# -*- coding: utf-8 -*-
# @Time    : 2018/4/7 下午1:44
# @author  : slark
# @File    : unitest_hello.py
# @Software: PyCharm
import unittest


class Dict(dict):
    def __init__(self, **kwargs):
        super(Dict, self).__init__(**kwargs)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute {}".format(item))

    def __setattr__(self, key, value):
        self[key] = value


class TestDict(unittest.TestCase):

    def test_init(self):
        d = Dict(a=1, b='test')
        self.assertEqual(d.a, 1)
        self.assertEqual(d.b, 'test')
        self.assertTrue(isinstance(d, dict))

    def test_key(self):
        d = Dict()
        d['key'] = 'value'
        self.assertEqual(d.key, 'value')

    def test_attr(self):
        d = Dict()
        d.key = 'value'
        self.assertTrue('key' in d)
        self.assertEqual(d['key'], 'value')

    def test_keyerror(self):
        d = Dict()
        with self.assertRaises(KeyError):  # 期待抛出指定的异常
            value = d['empty']

    def test_attrerror(self):
        d = Dict()
        with self.assertRaises(AttributeError):  # 期待抛出指定异常
            value = d.empty


if __name__ == "__main__":
    unittest.main()
