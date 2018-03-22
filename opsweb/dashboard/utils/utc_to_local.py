#!/usr/bin/env python
#coding=utf8

import pytz
from tzlocal import get_localzone
from datetime import *

def utc_to_local(utctime):
    
    '''
    utctime : datetime.datetime(2016, 6, 12, 5, 0, tzinfo=<UTC>)

    下面是将普通的 datetime 生成的时间 转为 utc 时间
    utc = pytz.utc
    t = datetime(x,x,x,x,x,x)
    utc_dt = utc.localize(t)
    '''

    tz = get_localzone()
    local_time = utctime.astimezone(tz)
    return local_time

def utc_to_local_sec(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%SZ'):
    local_tz = pytz.timezone('Asia/Chongqing')
    local_format = "%Y-%m-%d %H:%M"
    utc_dt = datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    return time_str

def utc_to_local_T(utc_time_str, utc_format='%Y-%m-%dT%H:%MZ'):
    local_tz = pytz.timezone('Asia/Chongqing')
    local_format = "%Y-%m-%d %H:%M"
    utc_dt = datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    return time_str
