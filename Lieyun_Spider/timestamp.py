# -*- coding: utf-8 -*-
import time

# timeArray = time.strptime(a, "%Y-%m-%d")
# timeStamp = int(time.mktime(timeArray))
# print timeArray.tm_year
def timestamp(original_time):
    time_og = time.localtime(time.time())
    current_time = str(time_og.tm_year) + '-' + str(time_og.tm_mon) + '-' + str(time_og.tm_mday)
    timeArray = time.strptime(current_time, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    if '小时' in original_time:
        a = original_time.split('小')
        a=int(a[0])
        if time_og.tm_hour-a>=0:

            return timeStamp
        else:
            timeStamp = timeStamp - 86400
            return timeStamp
    elif '天' in original_time:
        timeStamp = timeStamp - 86400
        return timeStamp
    else:
        timeArray = time.strptime(original_time, "%Y-%m-%d")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp










