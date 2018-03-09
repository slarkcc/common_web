# -*- coding: utf-8 -*-
# @Time    : 2018/2/27 16:31
# @author  : slark
# @File    : worker_task.py
# @Software: PyCharm
from multiprocessing.managers import BaseManager
import time, sys, Queue

BaseManager.register('get_task_queue')
BaseManager.register('get_result_queue')

server_addr = '127.0.0.1'
print('connecting to server %s' % server_addr)

m = BaseManager(address=(server_addr, 5000), authkey=b'abc')
m.connect()

task = m.get_task_queue()
result = m.get_result_queue()

for i in range(50):
    try:
        n = task.get(timeout=2)
        print('run task %d*%d' % (n, n))
        r = '%d * %d = %d' % (n, n, n * n)
        time.sleep(1)
        result.put(r)
    except Queue.Empty:
        print('task queue is empty.')

print("worker exit.")
