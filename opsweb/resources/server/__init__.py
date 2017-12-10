from django.views.generic import View,TemplateView,ListView
from django.http import JsonResponse
from resources.models import Server_Aliyun,IDC
from resources.forms import ServerAliyunAddForm
from api.thirdapi.ansible_adhoc import ansible_adhoc
from api.thirdapi.aliyun_describe_instance import AliyunDescribeInstances,AliyunDescribeInstanceAutoRenewAttribute
from django.forms.models import model_to_dict
import json
from datetime import *
from utc_to_local import utc_to_local

class ServerAliyunListView(ListView):
    template_name = "server/server_aliyun_list.html"
    model = Server_Aliyun
    paginate_by = 10
    ordering = 'id'


class ServerAliyunAddView(View):

    def post(self,request):
        ret = {"result":0,"msg":None}
        server_aliyun_add_form = ServerAliyunAddForm(request.POST)
        if not server_aliyun_add_form.is_valid():
            ret["result"] = 1
            ret["msg"] = json.dumps(json.loads(server_aliyun_add_form.errors.as_json(escape_html=False)),ensure_ascii=False)
            return JsonResponse(ret)
    
        try:
            server_aliyun_obj = Server_Aliyun(**server_aliyun_add_form.cleaned_data)
            server_aliyun_obj.save()
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = e.args
            return JsonResponse(ret)

        try:
            with open("/etc/ansible/hosts",'a+') as f:
                if "%s\n" %(server_aliyun_obj.private_ip) not in f.readlines():
                    f.write("%s:%s\n" %(server_aliyun_obj.private_ip,server_aliyun_obj.ssh_port))
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = e.args
        else:
            ret["msg"] = "服务器 %s 添加成功" %(server_aliyun_add_form.cleaned_data.get("private_ip"))
        return JsonResponse(ret)

class ServerAliyunRefreshView(View):
    
    def post(self,request):
        ret = {"result":0,"msg":None}
        server_id = request.POST.get("id",0)

        try:
            server_aliyun_obj = Server_Aliyun.objects.get(id__exact=server_id)
            private_ip = server_aliyun_obj.private_ip
        except Server_Aliyun.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "该服务器ID %s 不存在，请刷新重试" %(server_id)
            return JsonResponse(ret)
        
        try:
            server_info_ansible = ansible_adhoc('setup','gather_subset=hardware,!facter',private_ip)[private_ip]['ansible_facts']
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "ansible api 调用失败，请查看日志"
            return JsonResponse(ret)

        try:
            server_aliyun_obj.hostname = server_info_ansible['ansible_hostname']
            server_aliyun_obj.server_brand = server_info_ansible['ansible_system_vendor']
            server_aliyun_obj.swap = '%.2f GB' %(server_info_ansible['ansible_swaptotal_mb']/1024.0)
            server_aliyun_obj.disk = '</br>'.join(['['+i+'] '+': '+server_info_ansible['ansible_devices'][i]['size'] for i in server_info_ansible['ansible_devices'] if 'ss' in i or 'sd' in i or 'vd' in i])
            server_aliyun_obj.disk_mount = '\n'.join(['['+i['mount']+'] '+': %.2f GB' %(i['size_total']/1024.0/1024.0/1024.0) for i in server_info_ansible['ansible_mounts']])
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "ansible api 某个属性获取值失败，请查看日志"
            return JsonResponse(ret)

        try:
            server_info_aliyun = AliyunDescribeInstances(PrivateIpAddresses=[private_ip])[0]
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "aliyun api 调用失败，请查看日志"
            return JsonResponse(ret)

        try:
            server_aliyun_obj.public_ip = server_info_aliyun["PublicIpAddress"].get("IpAddress")[0] if server_info_aliyun["PublicIpAddress"].get("IpAddress") else server_info_aliyun["EipAddress"]["IpAddress"]
            server_aliyun_obj.instance_id = server_info_aliyun["InstanceId"]
            server_aliyun_obj.region = server_info_aliyun["RegionId"]
            server_aliyun_obj.zone = server_info_aliyun["ZoneId"]
            server_aliyun_obj.instance_type = server_info_aliyun["InstanceType"]
            server_aliyun_obj.os_version = server_info_aliyun["OSName"]
            server_aliyun_obj.cpu_count = '%s 核' %(server_info_aliyun["Cpu"])
            server_aliyun_obj.mem = '%.2f GB' %(server_info_aliyun["Memory"]/1024.0)
            server_aliyun_obj.charge_type = server_info_aliyun["InstanceChargeType"]
            server_aliyun_obj.status = server_info_aliyun["Status"]
            server_aliyun_obj.online_time = server_info_aliyun["CreationTime"]
            server_aliyun_obj.expired_time = server_info_aliyun["ExpiredTime"]
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "aliyun api 某个属性失败，请查看日志"
            #ret["msg"] = e.args
            return JsonResponse(ret)

        server_renewal_status = AliyunDescribeInstanceAutoRenewAttribute(server_info_aliyun["InstanceId"])
        if server_info_aliyun["InstanceChargeType"] == 'PostPaid':
            server_aliyun_obj.renewal_type = 'RenewalByUsed'
        elif server_renewal_status["result"] == 1:
            ret["result"] = 1
            ret["msg"] = "aliyun api 获取续费状态失败，请查看日志:server_renewal_status['msg']"
            return JsonResponse(ret)
        else:
            server_aliyun_obj.renewal_type = server_renewal_status["data"]

        try:
            server_aliyun_obj.save()
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "服务器信息刷新后保存数据库失败，请查看日志"
            #ret["msg"] = e.args
        else:
            ret["msg"] = "服务器信息刷新成功"

        return JsonResponse(ret)

class ServerAliyunInfoView(View):

    def get(self,request):
        ret = {"result":0,"msg":None}
        sid = request.GET.get("id",0)
        try:
            server_aliyun_obj = Server_Aliyun.objects.get(id__exact=sid)
        except Server_Aliyun.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "Aliyun 上不存在 ID 为 %s 的服务器" %(sid)
            return JsonResponse(ret)

        try:
            #server_aliyun_info = model_to_dict(server_aliyun_obj)  // 使用这个方法,读不到 DateTimeField 设置为 auto_now = True 的字段,因此读不到 last_update_time 字段
            server_aliyun_info = Server_Aliyun.objects.filter(id__exact=sid).values()[0]
            server_aliyun_info["idc"] = server_aliyun_obj.idc.cn_name
            server_aliyun_info["env"] = server_aliyun_obj.get_env_display()
            server_aliyun_info["charge_type"] = server_aliyun_obj.get_charge_type_display()
            server_aliyun_info["status"] = server_aliyun_obj.get_status_display()
            server_aliyun_info["renewal_type"] = server_aliyun_obj.get_renewal_type_display()
            server_aliyun_info["disk"] = server_aliyun_info["disk"].replace("</br>","\n")
            if server_aliyun_info.get("expired_time"):
                server_aliyun_info["expired_time"] = utc_to_local(server_aliyun_info["expired_time"]).strftime("%Y-%m-%d %X")
            if server_aliyun_info.get("offline_time"):
                server_aliyun_info["offline_time"] = utc_to_local(server_aliyun_info["offline_time"]).strftime("%Y-%m-%d %X")
            if server_aliyun_info.get("online_time"):
                server_aliyun_info["online_time"] = utc_to_local(server_aliyun_info["online_time"]).strftime("%Y-%m-%d %X")
            if server_aliyun_info.get("last_update_time"):
                server_aliyun_info["last_update_time"] = utc_to_local(server_aliyun_info["last_update_time"]).strftime("%Y-%m-%d %X")
        except Exception as e:
            ret["result"] = 1
            #ret["msg"] = "模型对象转dict失败" 
            ret['msg'] = e.args
        else:
            ret["server_info"] = server_aliyun_info

        return JsonResponse(ret)
