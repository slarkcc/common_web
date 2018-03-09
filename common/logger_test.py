# -*- coding: utf-8 -*-
# @Time    : 2018/3/1 10:21
# @author  : slark
# @File    : logger_test.py
# @Software: PyCharm


import logging
import sys, os


# # 获取logger实例，如果参数为空则返回root logger
# logger = logging.getLogger("AppName")
#
# # 指定logger输出格式
# formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
#
# # 文件日志
# file_handler = logging.FileHandler("test.log")
# file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
#
# # 控制台日志
# console_handler = logging.StreamHandler(sys.stdout)
# console_handler.formatter = formatter  # 也可以直接给formatter赋值
#
# # 为logger添加的日志处理器
# logger.addHandler(file_handler)
# logger.addHandler(console_handler)
#
# # 指定日志的最低输出级别，默认为WARN级别
# logger.setLevel(logging.INFO)
#
# # 输出不同级别的log
# logger.debug('this is debug info')
# logger.info('this is information')
# logger.warn('this is warning message')
# logger.error('this is error message')
# logger.fatal('this is fatal message, it is same as logger.critical')
# logger.critical('this is critical message')
#
# # 2016-10-08 21:59:19,493 INFO    : this is information
# # 2016-10-08 21:59:19,493 WARNING : this is warning message
# # 2016-10-08 21:59:19,493 ERROR   : this is error message
# # 2016-10-08 21:59:19,493 CRITICAL: this is fatal message, it is same as logger.critical
# # 2016-10-08 21:59:19,493 CRITICAL: this is critical message
#
# # 移除一些日志处理器
# logger.removeHandler(file_handler)
#################################################################################
# logger = logging.getLogger("simple_example")
# logger.setLevel(logging.DEBUG)
#
# fh = logging.FileHandler('spam.log')
# fh.setLevel(logging.DEBUG)
#
# ch = logging.StreamHandler()
# ch.setLevel(logging.ERROR)
#
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# ch.setFormatter(formatter)
# fh.setFormatter(formatter)
#
# logger.addHandler(ch)
# logger.addHandler(fh)
#
# logger.debug("debug message")
# logger.info('info message')
# logger.info('warn message')
# logger.error('error message')
# logger.critical('critical message')

######################################################################
class Logger(object):
    def __init__(self, path, clevel=logging.DEBUG, flevel=logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')

        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)

        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(flevel)

        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.critical(message)
