# coding=utf-8
from multiprocessing import Process, Pool, Queue, cpu_count

import os, time, random, subprocess, threading

lock = threading.Lock()


def run_proc(name):
    print("Run child process %s (%s)" % (name, os.getpid()))


def long_time_task(name):
    print("Run task %s (%s)..." % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print("Task %s run %0.f seconds." % (name, (end - start)))


def write(q):
    print("Process to write: %s" % os.getpid())
    for value in ['a', 'b', 'c']:
        print("Put %s to queue..." % value)
        q.put(value)
        time.sleep(random.random())


def read(q):
    print("Process to read: %s" % os.getpid())
    while True:
        value = q.get(True)
        print("Get %s from queue." % value)


def loop():
    print("thread %s is running..." % threading.current_thread().name)
    n = 0
    while n < 5:
        n += 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print("thread %s ended" % threading.current_thread().name)


balance = 0


def change_it(n):
    global balance
    balance = balance + n
    balance = balance - n
    print balance


def run_thread(n):
    for i in range(10000):
        change_it(n)


def run_thread_safe(n):
    for i in range(10000):
        lock.acquire()
        try:
            change_it(n)
        finally:
            lock.release()


# 死循环
def loop():
    x = 0
    while True:
        x = x ^ 1


local_school = threading.local()


def process_student():
    std = local_school.student
    print('hello, %s (in %s)' % (std, threading.current_thread().name))


def process_thread(name):
    local_school.student = name
    process_student()


if __name__ == "__main__":
    t1 = threading.Thread(target=process_thread, args=('Alice',), name='Thread-A')
    t2 = threading.Thread(target=process_thread, args=('Bob',), name='Thread-B')
    t1.start()
    t2.start()
    t1.join()
    t2.join()

# if __name__ == "__main__":
#
#     for i in range(cpu_count()):
#         t = threading.Thread(target=loop)
#         t.start()

# if __name__ == "__main__":
#     print("Parent process %s" % os.getpid())
#     p = Process(target=run_proc, args=('test_code',))
#     print('Child process will start')
#     p.start()
#     p.join()
#     print('Child process end.')


# if __name__ == "__main__":
#     print("Parent process %s." % os.getpid())
#     p = Pool(4)
#     for i in range(5):
#         p.apply_async(long_time_task, args=(i, ))
#     print("Waiting for all subprocess done...")
#     p.close()
#     p.join()
#     print("All subprocess done.")

#
# if __name__ == "__main__":
#     print("$ nslookup www.baidu.com")
#     r = subprocess.call(['nslookup', 'www.baidu.com'])
#     print("exit code:", r)


# if __name__ == "__main__":
#     q = Queue()  # q作为中间媒介
#     pw = Process(target=write, args=(q,))
#     pr = Process(target=read, args=(q,))
#     pw.start()
#     pr.start()
#     pw.join()
#     pr.terminate()


# if __name__ == "__main__":
#     print("thread %s is running..." % threading.current_thread().name)
#     t = threading.Thread(target=loop, name='LoopThread')
#     t.start()
#     t.join()
#     print('thread %s ended' % threading.current_thread().name)


# if __name__ == "__main__":
#     t1 = threading.Thread(target=run_thread, args=(5,))
#     t2 = threading.Thread(target=run_thread, args=(8,))
#     t1.start()
#     t2.start()
#     t1.join()
#     t2.join()
#     print(balance)
