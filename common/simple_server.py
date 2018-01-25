# -*- coding: utf-8 -*-
# @Time    : 2018/1/24 16:29
# @author  : slark
# @File    : simple_server.py
# @Software: PyCharm
from wsgiref.simple_server import make_server


def application(environ, start_response):
    """
    HTTP请求的所有输入信息都可以通过environ获得，HTTP响应的输出都可以通过start_response()加上函数返回值作为Body
    :param environ:
    :param start_response:
    :return:
    """
    start_response('200 ojk', [('Content-Type', 'text/html')])
    return '<h1>Hello, web!</h1>'


hpptd = make_server('', 8000, application)

print "Serving HTTP on port 8000..."

hpptd.serve_forever()
