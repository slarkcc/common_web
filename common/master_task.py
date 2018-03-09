# -*- coding: utf-8 -*-
# @Time    : 2018/2/27 15:03
# @author  : slark
# @File    : master_task.py
# @Software: PyCharm

import random, time, Queue
import multiprocessing

from multiprocessing.managers import BaseManager

task_queue = Queue.Queue()
result_queue = Queue.Queue()

BaseManager.register('get_task_queue', callable=lambda: task_queue)
BaseManager.register('get_result_queue', callable=lambda: result_queue)

manager = BaseManager(address=('', 5000), authkey=b'abc')

manager.start()

task = manager.get_task_queue()
result = manager.get_result_queue()

begin_time = time.time()

for i in range(50):
    r = random.randint(10001, 99999)
    print("Put task %d ..." % r)
    task.put(r)

for i in range(50):
    r = result.get(timeout=10)
    print('Result is %s' % r)

manager.shutdown()

print("master exit.")
end_time = time.time()
print('costtime: %0.5f' % (end_time - begin_time))
