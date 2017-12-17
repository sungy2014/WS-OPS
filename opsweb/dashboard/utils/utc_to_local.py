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
