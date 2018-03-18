# -*- coding: utf-8 -*-
# @Time    : 2018/3/13 16:49
# @author  : slark
# @File    : asyncio_hello.py
# @Software: PyCharm

# 定义一个协程
import time
import asyncio

now = lambda: time.time()


async def do_some_thing(x):
    print("Waiting:", x)


start = now()

coroutine = do_some_thing(2)

loop = asyncio.get_event_loop()
loop.run_until_complete(coroutine)

print('TIME:', now() - start)

# 创建一个task
import asyncio
import time

now = lambda: time.time()


async def do_some_work(x):
    print("Waiting:", x)


start = now()

coroutine = do_some_work(2)
loop = asyncio.get_event_loop()

task = loop.create_task(coroutine)
print(task)

loop.run_until_complete(task)
print(task)

print('Time:', now() - start)

# 绑定回调

import time
import asyncio
from functools import partial

now = lambda: time.time()


async def do_some_work(x):
    print("Waiting:", x)
    return "Done after {}s".format(x)


def callback(future):
    print("Callback: ", future.result())


def callback1(t, future):
    print("Callback: ", t, future.result())


start = now()

coroutine = do_some_work(3)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(coroutine)
# task.add_done_callback(callback)
task.add_done_callback(partial(callback1, 2))
loop.run_until_complete(task)

print('Time:', now() - start)


# future与result

async def do_some_thing(x):
    print("Waiting {}".format(x))
    return "Done after {}s".format(x)


start = now()

coroutine = do_some_thing(3)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(coroutine)
loop.run_until_complete(task)

print("Task ret:{}".format(task.result()))
print("Time: {}".format(now() - start))

# 阻塞和await
import asyncio
import time


async def do_some_work(x):
    print("Waiting: ", x)
    await asyncio.sleep(x)
    return "Done after {}s".format(x)


start = time.time()

coroutine = do_some_work(2)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(coroutine)
loop.run_until_complete(task)

print("Task ret:", task.result())
print("TIME:", time.time() - start)

#  并行和并发
import asyncio
import time


async def do_some_work(x):
    print("Waiting: ", x)

    await asyncio.sleep(x)
    return "Done after {}s".format(x)


start = time.time()
coro1 = do_some_work(1)
coro2 = do_some_work(2)
coro3 = do_some_work(3)

tasks = [
    asyncio.ensure_future(coro1),
    asyncio.ensure_future(coro2),
    asyncio.ensure_future(coro3),
]

loop = asyncio.get_event_loop()

loop.run_until_complete(asyncio.wait(tasks))

for task in tasks:
    print("Task ret:", task.result())

print("Time: ", time.time() - start)

# 协程嵌套
import asyncio
import time

start = time.time()


async def do_some_work(x):
    print("Waiting: ", x)

    await asyncio.sleep(x)
    return "Done after {}s".format(x)


async def main():
    coro1 = do_some_work(1)
    coro2 = do_some_work(2)
    coro3 = do_some_work(4)

    tasks = [
        asyncio.ensure_future(coro1),
        asyncio.ensure_future(coro2),
        asyncio.ensure_future(coro3),
    ]

    done, pending = await asyncio.wait(tasks)

    for task in done:
        print("Task ret: ", task.result())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

print("Time: ", time.time() - start)

# 协程停止
start = time.time()


async def do_some_work(x):
    print("Waiting: ", x)

    await asyncio.sleep(x)
    return "Done after {}s".format(x)


coro1 = do_some_work(1)
coro2 = do_some_work(2)
coro3 = do_some_work(4)

tasks = [
    asyncio.ensure_future(coro1),
    asyncio.ensure_future(coro2),
    asyncio.ensure_future(coro3),
]

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(asyncio.wait(tasks))
except KeyboardInterrupt as e:
    for task in asyncio.Task.all_tasks():
        print(task.cancel())
    loop.stop()
    loop.run_forever()

finally:
    loop.close()

print("Time: ", time.time() - start)

# 不同线程的事件循环
from threading import Thread


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def more_work(x):
    print("More work {}".format(x))
    time.sleep(x)
    print("Finished more work {}".format(x))


start = time.time()
new_loop = asyncio.get_event_loop()

t = Thread(start_loop, args=(new_loop,))
t.start()
print("Time: {}".format(time.time() - start))

new_loop.call_soon_threadsafe(more_work, 6)
new_loop.call_soon_threadsafe(more_work, 3)