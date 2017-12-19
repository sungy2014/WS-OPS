#!/usr/bin/env python

import sys,os
from dashboard.utils.wslog import wslog_error,wslog_info
from resources.models import ServerAliyunModel
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

if __name__ == "__main__":
    ServerAliyunAutoAddCrontab()
