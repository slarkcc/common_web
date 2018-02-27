# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:26
# @author  : slark
# @File    : date_function.py
# @Software: PyCharm


from datetime import datetime, timedelta, date
import calendar

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday']


def get_previous_byday(dayname, start_date=None):
    """
    查找最后一个周几出现的日期
    :param dayname:
    :param start_date:
    :return:
    """
    if start_date is None:
        start_date = datetime.today()
    day_num = start_date.weekday()
    day_num_target = weekdays.index(dayname)
    days_ago = (7 + day_num - day_num_target) % 7
    if days_ago == 0:
        days_ago = 7
    target_date = start_date - timedelta(days=days_ago)
    return target_date


def get_month_range(start_date=None):
    """

    :param start_date:
    :return:
    """
    if not start_date:
        start_date = date.today().replace(day=1)
    _, day_in_month = calendar.monthrange(start_date.year, start_date.month)
    end_date = start_date + timedelta(days=day_in_month)
    return start_date, end_date
