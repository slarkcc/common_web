# -*- coding: utf-8 -*-
# @Time    : 2018/1/26 11:10
# @author  : slark
# @File    : multiprocess_.py
# @Software: PyCharm
import os, time, random
from multiprocessing import Pool


def process_task(name):
    print "Run task %s in progress id : %s" % (name, os.getpid())
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print "task %s runs in %0.2f" % (name, (end - start))


if __name__ == '__main__':
    print "parent process id: %s" % (os.getpid())
    pool = Pool()
    for i in range(5):
        pool.apply_async(process_task, args=(i,))
    print "Waiting all process done..."
    pool.close()
    pool.join()
    print "All process done"
