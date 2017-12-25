#!/usr/bin/env python

import sys
import os
from datetime import *
from dashboard.utils.wslog import wslog_error,wslog_info
from resources.models import ServerAliyunModel,CmdbModel,ServerStatisticByDayModel,CmdbStatisticByDayModel
from resources.server import GetServerInfoFromApi

def ServerAliyunAutoAddCrontab():

    from resources.server import ServerAliyunAutoAdd
    ServerAliyunAutoAdd()

def ServerAliyunAutoRefreshCrontab():

    id_list = [i["id"] for i in ServerAliyunModel.objects.values("id")]
    for id in id_list:
        try:
            server_aliyun_obj = ServerAliyunModel.objects.get(id__exact=id)
            private_ip = server_aliyun_obj.private_ip
        except Exception as e:
            wslog_error().error("获取server_aliyun 对象失败,错误信息: %s" %(e.args))
            continue

        ret = GetServerInfoFromApi(private_ip,server_aliyun_obj)

        if ret["result"] == 1:
            wslog_error().error("服务器: %s 自动刷新失败,错误信息: %s" %(private_ip,ret["msg"]))
            continue
        else:
            wslog_info().info("服务器: %s 自动刷新成功" %(private_ip))

def ServerStatisticByDayCrontab():
    myday = date.today().isoformat()
    my_yesterday = (date.today() - timedelta(days=1)).isoformat()
    count = ServerAliyunModel.objects.count()

    try:
        s_obj = ServerStatisticByDayModel.objects.get(myday__exact=my_yesterday).count
    except ServerStatisticByDayModel.DoesNotExist:
        count_yesterday = 0
    else:
        count_yesterday = s_obj.count

    compared_with_yesterday = count - count_yesterday

    ssbd_obj = ServerStatisticByDayModel()

    try:
        ssbd_obj.myday = myday
        ssbd_obj.count = count
        ssbd_obj.compared_with_yesterday = compared_with_yesterday
        ssbd_obj.save()
    except Exception as e:
        wslog_error().error("统计 %s 的服务器总数失败,错误信息: %s" %(myday,e.args))
        sys.exit()
    else:
        wslog_info().info("统计 %s 的服务器总数成功" %(myday))
    

def CmdbStatisticByDayCrontab():
    myday = date.today().isoformat()
    my_yesterday = (date.today() - timedelta(days=1)).isoformat()
    count = CmdbModel.objects.count()

    try:
        s_obj = CmdbStatisticByDayModel.objects.get(myday__exact=my_yesterday).count
    except CmdbStatisticByDayModel.DoesNotExist:
        count_yesterday = 0
    else:
        count_yesterday = s_obj.count

    compared_with_yesterday = count - count_yesterday

    csbd_obj = CmdbStatisticByDayModel()

    try:
        csbd_obj.myday = myday
        csbd_obj.count = count
        csbd_obj.compared_with_yesterday = compared_with_yesterday
        csbd_obj.save()
    except Exception as e:
        wslog_error().error("统计 %s 的应用总数失败,错误信息: %s" %(myday,e.args))
        sys.exit()
    else:
        wslog_info().info("统计 %s 的应用总数成功" %(myday))
 

    return ''

if __name__ == "__main__":
    ServerStatisticByDayCrontab()
