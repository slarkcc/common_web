# -*- coding: utf-8 -*-
# @Time    : 2018/5/25 21:53
# @author  : slark
# @File    : util.py
# @Software: PyCharm

def get_path(filename):
    """
    :return files'path or empty string if no path
    :param filename:
    :return:
    """
    import os
    head, tail = os.path.split(filename)
    return head