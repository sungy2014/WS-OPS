#!/usr/bin/env python

import sys
import os
from datetime import *
from dashboard.utils.wslog import wslog_error,wslog_info
from resources.models import ServerModel,CmdbModel,ServerStatisticByDayModel,CmdbStatisticByDayModel
from resources.server import GetServerInfoFromApi

def ServerAliyunAutoAddCrontab():

    from resources.server import ServerAliyunAutoAdd
    ServerAliyunAutoAdd()

def ServerAliyunAutoRefreshCrontab():

    id_list = [i["id"] for i in ServerModel.objects.values("id")]
    for id in id_list:
        try:
            server_aliyun_obj = ServerModel.objects.get(id__exact=id)
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
    count = ServerModel.objects.count()

    try:
        s_obj = ServerStatisticByDayModel.objects.get(myday__exact=my_yesterday)
    except ServerStatisticByDayModel.DoesNotExist:
        count_yesterday = 0
    else:
        count_yesterday = s_obj.count

    compared_with_yesterday = count - count_yesterday

    ssbd_obj = ServerStatisticByDayModel()

    try:
        ssbd_obj.myday = myday
        ssbd_obj.count = count
        ssbd_obj.compared_with_yesterday = str(compared_with_yesterday)
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
        s_obj = CmdbStatisticByDayModel.objects.get(myday__exact=my_yesterday)
    except CmdbStatisticByDayModel.DoesNotExist:
        count_yesterday = 0
    else:
        count_yesterday = s_obj.count

    compared_with_yesterday = count - count_yesterday

    csbd_obj = CmdbStatisticByDayModel()

    try:
        csbd_obj.myday = myday
        csbd_obj.count = count
        csbd_obj.compared_with_yesterday = str(compared_with_yesterday)
        csbd_obj.save()
    except Exception as e:
        wslog_error().error("统计 %s 的应用总数失败,错误信息: %s" %(myday,e.args))
        sys.exit()
    else:
        wslog_info().info("统计 %s 的应用总数成功" %(myday))
 

def CmdbAutoAddCrontab():
    server_ip_name_list = list(ServerModel.objects.values("id","private_ip","instance_name","status"))

    #根据 CmdbModel 模型中的 instance_name 字段自动添加 CMDB,如果没有该字段则不能自动添加 CMDB,
    #因此该方法适用于 Aliyun 上的服务器，IDC中的服务器需要手动添加，该方法也不会修改IDC服务器 CMDB 的信息
    for ss in server_ip_name_list:
        try:
            ss_obj = ServerModel.objects.get(id__exact=ss["id"])
        except Exception as e:
            wslog_error().error("获取服务器 %s 对象失败,错误信息: %s" %(ss["private_ip"],e.args))
            continue 

        if ss["status"] != "Running":
            wslog_info().info("该服务器: %s 状态 %s 所以需要删除其关联的CMDB" %(ss["private_ip"],ss["status"]))
            ss_obj.cmdbmodel_set.clear()
            continue            

        if not ss["instance_name"]:
            wslog_error().error("该服务器: %s 没有实例名" %(ss["private_ip"]))
            continue

        app_name_list = ss["instance_name"].split("_")[-2::-1]
        if not app_name_list:
            wslog_error().error("该服务器: %s 实例名 %s 格式不正确" %(ss["private_ip"],ss["instance_name"]))
            continue

        cmdb_name_list = [i["name"] for i in list(CmdbModel.objects.values("name"))]

        cmdb_obj_list = []
        for app in app_name_list:
            cmdb_data = {"way":"tomcat","type":"1","env":"online","status":"0","ports":"8080"}
            if not cmdb_name_list:
                cmdb_data["name"] = app
                try:
                    cc = CmdbModel(**cmdb_data)
                    cc.ips.set([ss_obj])
                    cc.save()
                except Exception as e:
                    wslog_error().error("CmdbModel 自动添加失败,错误信息: %s" %(e.args))
                    continue
                else:
                    wslog_info().info("CmdbModel 自动添加对象 %s 并关联 ServerModel 成功" %(app))
                    continue

            if app in cmdb_name_list:
                try:
                    cmdb_obj = CmdbModel.objects.get(name__exact=app)
                except Exception as e:
                    wslog_error().error("CmdbModel 查询对象 %s 失败,错误信息: %s" %(app,e.args))
                    continue
                cmdb_obj_list.append(cmdb_obj)
            else:
                cmdb_data["name"] = app
                try:
                    cm_obj = CmdbModel(**cmdb_data)
                    cm_obj.save()
                except Exception as e:
                    wslog_error().error("CmdbModel 自动添加失败,错误信息: %s" %(e.args))
                    continue
                else:
                    wslog_info().info("CmdbModel 自动添加对象 %s 成功" %(app))
                    cmdb_obj_list.append(cm_obj)
        if cmdb_obj_list:
            ss_obj.cmdbmodel_set.set(cmdb_obj_list)

        try:
            CmdbModel.objects.filter(ips__private_ip__exact=None).delete()
        except Exception as e:
            wslog_error().error("CmdbModel 自动删除关联IP为空的对象失败,错误信息: %s" %(e.args))
                
                       
if __name__ == "__main__":
    ServerStatisticByDayCrontab()
