from django.views.generic import View,TemplateView,ListView
from django.http import JsonResponse
from resources.models import ServerAliyunModel,IDC,ServerIdcModel,CmdbModel
from resources.forms import ServerAliyunAddForm,ServerAliyunUpdateForm
from api.thirdapi.ansible_adhoc import ansible_adhoc
from api.thirdapi.aliyun_describe_instance import AliyunDescribeInstances,AliyunDescribeInstanceAutoRenewAttribute
from django.forms.models import model_to_dict
import json
from datetime import *
from dashboard.utils.utc_to_local import utc_to_local
from dashboard.utils.wslog import wslog_error,wslog_info
from django.db.models import Q


def GetServerInfoFromApi(private_ip,server_aliyun_obj):
    
    ret = {"result":0,"msg":None}
    try:
        server_info_ansible = ansible_adhoc('setup','gather_subset=hardware,!facter',private_ip)[private_ip]['ansible_facts']
    except Exception as e:
        ret["result"] = 1
        ret["msg"] = "ansible api 调用失败，请查看日志"
        wslog_error().error(e.args)
        return ret

    try:
        server_aliyun_obj.hostname = server_info_ansible['ansible_hostname']
        server_aliyun_obj.server_brand = server_info_ansible['ansible_system_vendor']
        server_aliyun_obj.swap = '%.2f GB' %(server_info_ansible['ansible_swaptotal_mb']/1024.0)
        server_aliyun_obj.disk = '</br>'.join(['['+i+'] '+': '+server_info_ansible['ansible_devices'][i]['size'] for i in server_info_ansible['ansible_devices'] if 'ss' in i or 'sd' in i or 'vd' in i])
        server_aliyun_obj.disk_mount = '\n'.join(['['+i['mount']+'] '+': %.2f GB' %(i['size_total']/1024.0/1024.0/1024.0) for i in server_info_ansible['ansible_mounts']])
    except Exception as e:
        ret["result"] = 1
        ret["msg"] = "ansible api 某个属性获取值失败，请查看日志"
        wslog_error().error(e.args)
        return ret 
    
    try:
        server_info_aliyun = AliyunDescribeInstances(PrivateIpAddresses=[private_ip])[0]
    except Exception as e:
        ret["result"] = 1
        ret["msg"] = "aliyun api 调用失败，请查看日志"
        wslog_error().error(e.args)
        return ret

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
        wslog_error().error(e.args)
        return ret

    server_renewal_status = AliyunDescribeInstanceAutoRenewAttribute(server_info_aliyun["InstanceId"])
    if server_info_aliyun["InstanceChargeType"] == 'PostPaid':
        server_aliyun_obj.renewal_type = 'RenewalByUsed'
    elif server_renewal_status["result"] == 1:
        ret["result"] = 1
        ret["msg"] = "aliyun api 获取续费状态失败，请查看日志"
        return ret
    else:
        server_aliyun_obj.renewal_type = server_renewal_status["data"]

    try:
        server_aliyun_obj.save()
    except Exception as e:
        ret["result"] = 1
        ret["msg"] = "服务器信息刷新后保存数据库失败，请查看日志"
        wslog_error().error(e.args)
    else:
        ret["msg"] = "服务器信息刷新成功"

    return ret

class ServerAliyunListView(ListView):
    template_name = "server/server_aliyun_list.html"
    model = ServerAliyunModel
    paginate_by = 10
    ordering = 'id'
    page_total = 11

    def get_context_data(self,**kwargs):
        context = super(ServerAliyunListView,self).get_context_data(**kwargs)
        context['page_range'] = self.get_page_range(context['page_obj'])
        # request.GET 是获取QueryDict对象,也即是前端传过来的所有参数,由于QueryDict对象是只读的,所有要使用copy方法,赋值一份出来,才能进行修改
        search_data = self.request.GET.copy()
        try:
            search_data.pop('page')
        except:
            pass

        if search_data:
            context['search_uri'] = '&' + search_data.urlencode()
        else:
            context['search_uri'] = '' 
        # context.update(字典A) 是合并字典 context 和 A
        context.update(search_data.dict())
        return context

    # 过滤模型中的数据
    def get_queryset(self):
        queryset = super(ServerAliyunListView,self).get_queryset()

        search_name = self.request.GET.get('search',None)
        if search_name:
            queryset = queryset.filter(Q(private_ip__icontains=search_name)|Q(public_ip__icontains=search_name)|Q(hostname__icontains=search_name))
        return queryset
    
    # 获取要展示的页数范围,这里是固定显示多少页
    def get_page_range(self,page_obj):
        page_now = page_obj.number
        if page_obj.paginator.num_pages > self.page_total:
            page_start = page_now - self.page_total//2
            page_end = page_now + self.page_total//2 + 1

            if page_start <= 0:
                page_start = 1
                page_end = page_start + self.page_total
            if page_end > page_obj.paginator.num_pages:
                page_end = page_obj.paginator.num_pages + 1
                page_start = page_end - self.page_total
        else:
            page_start = 1
            page_end = page_obj.paginator.num_pages + 1

        page_range = range(page_start,page_end)
        return page_range

class ServerAliyunAddView(View):

    def post(self,request):
        ret = {"result":0,"msg":None}
        server_aliyun_add_form = ServerAliyunAddForm(request.POST)
        if not server_aliyun_add_form.is_valid():
            ret["result"] = 1
            ret["msg"] = json.dumps(json.loads(server_aliyun_add_form.errors.as_json(escape_html=False)),ensure_ascii=False)
            return JsonResponse(ret)

        try:
            server_aliyun_obj = ServerAliyunModel(**server_aliyun_add_form.cleaned_data)
            server_aliyun_obj.save()
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = e.args
            return JsonResponse(ret)

        try:
            with open("/etc/ansible/hosts",'a+') as f:
                f.seek(0)
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
            server_aliyun_obj = ServerAliyunModel.objects.get(id__exact=server_id)
        except ServerAliyunModel.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "该服务器ID %s 不存在，请刷新重试" %(server_id)
            return JsonResponse(ret)
        else:
            private_ip = server_aliyun_obj.private_ip
        
        ret = GetServerInfoFromApi(private_ip,server_aliyun_obj)

        return JsonResponse(ret)

class ServerAliyunInfoView(View):

    def get(self,request):
        ret = {"result":0,"msg":None}
        sid = request.GET.get("id",0)
        try:
            server_aliyun_obj = ServerAliyunModel.objects.get(id__exact=sid)
        except ServerAliyunModel.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "Aliyun 上不存在 ID 为 %s 的服务器" %(sid)
            return JsonResponse(ret)

        try:
            #server_aliyun_info = model_to_dict(server_aliyun_obj)  // 使用这个方法,读不到 DateTimeField 设置为 auto_now = True 的字段,因此读不到 last_update_time 字段
            server_aliyun_info = ServerAliyunModel.objects.filter(id__exact=sid).values()[0]
            server_aliyun_info["env"] = {"id": server_aliyun_obj.env,"name": server_aliyun_obj.get_env_display()}
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
            ret["msg"] = "模型对象转dict失败" 
            wslog_error().error(e.args)
        else:
            ret["server_info"] = server_aliyun_info

        return JsonResponse(ret)

class ServerAliyunDeleteView(View):
    
    def post(self,request):
        ret = {"result":0,"msg":None}
        sid = request.POST.get('id',0)

        try:
            server_aliyun_obj = ServerAliyunModel.objects.get(id__exact=sid)
        except ServerAliyunModel.DoesNotExist:
            ret["result"] = 1
            ret["mag"] = "该服务器ID %s 不存在,请刷新重试" %(sid)
            return JsonResponse(ret)
        
        try:
            server_aliyun_obj.delete()
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = e.args
        else:
            ret["msg"] = "服务器 %s 删除成功" %(server_aliyun_obj.private_ip)

        return JsonResponse(ret)

class ServerAliyunUpdateView(View):

    def get(self,request):

        ret = {"result":0,"msg":None}
        server_info = {}
        sid = request.GET.get("id",0)

        try:
            server_aliyun_obj = ServerAliyunModel.objects.get(id__exact=sid)
        except ServerAliyunModel.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "Aliyun 上不存在 ID 为 %s 的服务器" %(sid)
            return JsonResponse(ret)

        try:
            server_info["id"] = sid
            server_info["private_ip"] = server_aliyun_obj.private_ip
            server_info["ssh_port"] = server_aliyun_obj.ssh_port   
            server_info["env"] = {"id": server_aliyun_obj.env,"name": server_aliyun_obj.get_env_display()}
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "从模型 ServerAliyun 中获取 id 为 %s 的数据失败" %(sid)
        else:
            ret["server_info"] = server_info

        return JsonResponse(ret)

    def post(self,request):
        ret = {"result":0,"msg":None}
        sid = request.POST.get('id',0)
        server_aliyun_update_form = ServerAliyunUpdateForm(request.POST)

        if not server_aliyun_update_form.is_valid():
            ret["result"] = 1
            ret["msg"] = json.dumps(json.loads(server_aliyun_update_form.errors.as_json(escape_html=False)),ensure_ascii=False)
            return JsonResponse(ret)

        try:
            server_aliyun_obj = ServerAliyunModel.objects.get(id__exact=sid)
        except ServerAliyunModel.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "服务器ID %s 不存在,请刷新重试" %(sid)
            return JsonResponse(ret)
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = e.args
            return JsonResponse(ret)
        
        try:
            server_aliyun_obj.hostname = server_aliyun_update_form.cleaned_data.get("hostname")
            server_aliyun_obj.ssh_port = server_aliyun_update_form.cleaned_data.get("ssh_port")
            server_aliyun_obj.env = server_aliyun_update_form.cleaned_data.get("env")
            server_aliyun_obj.save(update_fields=["hostname","ssh_port","env","last_update_time"])

        except Exception as e:
            ret["result"] = 1
            ret["msg"] = e.args
        else:
            ret["msg"] = "服务器 %s 更新成功" %(server_aliyun_obj.private_ip)

        return JsonResponse(ret)


def ServerAliyunAutoAdd():
    
    local_result = ServerAliyunModel.objects.values("private_ip")
    local_server_list = [i['private_ip'] for i in local_result]
    local_server_add = []
    local_server_delete = []

    try:
        aliyun_result = AliyunDescribeInstances()
    except Exception as e:
        wslog_error().error("服务器自动添加失败,错误信息: %s" %(e.args))
    else:
        aliyun_ecs_list = [i["NetworkInterfaces"]["NetworkInterface"][0]["PrimaryIpAddress"] for i in aliyun_result]
        local_server_add = list(set(aliyun_ecs_list).difference(set(local_server_list)))
        local_server_delete = list(set(local_server_list).difference(set(aliyun_ecs_list)))


    #添加服务器到本地 ServerAliyunModel 模型
    if local_server_add:
        for s in local_server_add:
            server = ServerAliyunModel()
            server.private_ip = s
            try:
                server.save()
            except Exception as e:
                wslog_error().error("自动添加服务器: %s,错误信息: %s" %(s,e.args))
                continue

            try:
                with open("/etc/ansible/hosts",'a+') as f:
                    f.seek(0)
                    if "%s\n" %(s) not in f.readlines():
                        f.write("%s\n" %(s))
            except Exception as e:
                wslog_error().error("自动添加服务器: %s,错误信息: %s" %(s,e.args))
                continue
            else:
                wslog_info().info("服务器: %s 自动添加成功" %(s))
                continue

    #将在阿里云上不存在的服务器,从本地的 ServerAliyunModel 模型中删除
    if local_server_delete:
        for s in local_server_delete:
            try:
                server_obj = ServerAliyunModel.objects.get(private_ip__exact=s)
            except ServerAliyunModel.DoesNostExist:
                wslog_error().error("自动删除服务器: %s ,已经不存在,所以不用删除" %(s))
                continue
            except Exception as e:
                wslog_error().error("自动删除服务器: %s,错误信息:%s" %(s,e.args))
                continue
            try:
                server_obj.delete()
            except Exception as e:
                wslog_error().error("自动删除服务器: %s,错误信息: %s" %(s,e.args))
                continue
            else:
                wslog_info().info("服务器: %s 自动删除成功" %(s))
                continue

