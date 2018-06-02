# -*- coding: utf-8 -*-
# @Time    : 2018/5/25 21:58
# @author  : slark
# @File    : example4.py
# @Software: PyCharm

# import util
#
# filename = __file__
#
# import pdb; pdb.set_trace()
#
# filename_path = util.get_path(filename)
# print(f'path = {filename_path}')


import os


def get_path(fname):
    """
    :return file's path or empty string if no path
    :param fname:
    :return:
    """
    import pdb
    pdb.set_trace()
    head, tail = os.path.split(fname)
    for char in tail:
        pass
    return head


filename = __file__
filename_path = get_path(filename)

print(f'path = {filename_path}')
