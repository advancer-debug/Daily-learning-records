# -*- coding = utf-8 -*-
# /usr/bin/env python
import datetime
import time


def get_last_month_first_day_v2(timestamp):
    """获取上一个月１号"""
    # 时间戳转化
    time_date = datetime.datetime.utcfromtimestamp(timestamp)
    first_day = datetime.date(time_date.year, time_date.month, 1)
    pre_month_day = first_day - datetime.timedelta(days=1)
    first_day_of_pre_month = datetime.date(pre_month_day.year, pre_month_day.month, 1)
    pre_month = str(pre_month_day.year)+'-'+str(pre_month_day.month)
    first_day_of_pre_month_hour = str(first_day_of_pre_month)+' '+'00:00:00'
    last_day_of_pre_month_hour = str(pre_month_day)+' '+'23:30:30'
    print(first_day_of_pre_month_hour)
    print(type(first_day_of_pre_month_hour))
    # first_day_time = time.strptime(first_day_of_pre_month_hour, "%Y-%m-%d %H:%M:%S")
    last_day_time = time.strptime(last_day_of_pre_month_hour, "%Y-%m-%d %H:%M:%S")
    # first_day_time_stamp = int(time.mktime(first_day_time))
    last_day_time_stamp = int(time.mktime(last_day_time))
    return pre_month, last_day_time_stamp


if __name__ == '__main__':
    timestamp = 1585582230
    print(timestamp)
    # 上个月的第一天
    result = get_last_month_first_day_v2(timestamp)
    print(result[0])
    print(result[1])
