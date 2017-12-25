from django.views.generic import View,TemplateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from resources.models import CmdbModel,ServerAliyunModel
from resources.forms import CmdbAddForm,CmdbUpdateForm
from dashboard.utils.wslog import wslog_error,wslog_info
from dashboard.utils.utc_to_local import utc_to_local
import json
from django.forms.models import model_to_dict
from django.db.models import Q

def GetCmdbObj(cid,ret):
    try:
        cmdb_obj = CmdbModel.objects.get(id__exact=cid)
    except CmdbModel.DoesNotExist:
        ret["result"] = 1
        ret["msg"] = "CmdbModel 不存在 ID: %s 的对象，请刷新重试" %(cid)
        wslog_error().error("CmdbModel 不存在 ID: %s 的对象" %(cid))
    else:
        ret["msg"] = cmdb_obj

    return ret

def CmdbIpsUpdate(ips,cmdb_obj,ret):
    if not ips:
        ret["result"] = 1
        ret["msg"] = "请至少选择一个IP"
        return ret

    try:
        server_obj_list = [ServerAliyunModel.objects.get(id__exact=sid) for sid in ips]
    except Exception as e:
        ret["result"] = 1
        ret["msg"] = "ServerAliyunModel 查询对象失败，请刷新并重新选择IP地址"
        wslog_error().error("ServerAliyunModel 查询对象地址失败" %(e.args))
        return ret

    try:
        cmdb_obj.save()
        cmdb_obj.ips.set(server_obj_list)
    except Exception as e:
        ret["result"] = 1
        ret["msg"] = "CmdbModel模型对象: %s 关联 ServerAliyunModel 失败,请查看日志" %(cmdb_obj.name)
        wslog_error().error("CmdbModel 模型对象: %s 关联 ServerAliyunModel 失败,错误信息: %s" %(cmdb_obj.name,e.args))
    finally:
        return ret

class CmdbListView(LoginRequiredMixin,ListView):
    template_name = "cmdb/cmdb_list.html"
    model = CmdbModel
    paginate_by = 10

    page_total = 11

    def get_context_data(self,**kwargs):
        context = super(CmdbListView,self).get_context_data(**kwargs)
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
        queryset = super(CmdbListView,self).get_queryset()

        search_name = self.request.GET.get('search',None)
        if search_name:
            queryset = queryset.filter(Q(name__icontains=search_name)|Q(ports__icontains=search_name)|Q(ips__private_ip__icontains=search_name)).distinct()
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

class CmdbAddView(LoginRequiredMixin,TemplateView):
    template_name = "cmdb/cmdb_add.html"

    def get_context_data(self,**kwargs):
        context = super(CmdbAddView,self).get_context_data(**kwargs)
        context["server_ips"] = [ {"id":i["id"],"private_ip":i['private_ip']} for i in ServerAliyunModel.objects.values("id","private_ip")]
        context["type"] = dict(CmdbModel.TYPE_CHOICES)
        context["env"] = dict(CmdbModel.ENV_CHOICES)
        context["way"] = dict(CmdbModel.WAY_CHOICES)
        return context
        
    def post(self,request):

        ret = {"result":0,"msg":None}
        cmdb_add_form = CmdbAddForm(request.POST)

        if not cmdb_add_form.is_valid():
            ret["result"] = 1
            ret["msg"] = json.dumps(json.loads(cmdb_add_form.errors.as_json(escape_html=False)),ensure_ascii=False)
            return JsonResponse(ret)

        try:
            cmdb_obj = CmdbModel(**cmdb_add_form.cleaned_data)
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "CmdbModel 模型对象: %s 添加失败,请查看日志" %(cmdb_add_form.cleaned_data.get("name"))
            wslog_error().error("CmdbModel 模型对象: %s 添加失败，错误信息: %s" %(cmdb_add_form.cleaned_data.get("name"),e.args))
            return JsonResponse(ret)

        ips = request.POST.getlist("ips")
        
        ret = CmdbIpsUpdate(ips,cmdb_obj,ret)

        if ret["result"] == 0:            
            ret["msg"] = "cmdb 模型对象: %s 添加成功" %(cmdb_add_form.cleaned_data.get("name"))
            wslog_info().info("CmdbModel 模型对象: %s 添加成功" %(cmdb_add_form.cleaned_data.get("name")))

        return JsonResponse(ret)

class CmdbChangeView(LoginRequiredMixin,View):

    def get(self,request):
        ret = {"result":0,"msg":None}
        cid = request.GET.get("id")
        
        ret = GetCmdbObj(cid,ret)
        if ret["result"] == 1:
            return JsonResponse(ret)

        cmdb_obj = ret["msg"]

        try:
            ips_list = [{"id":i["id"],"private_ip":i['private_ip']} for i in ServerAliyunModel.objects.filter(env__exact=cmdb_obj.env,status__exact="Running").values("id","private_ip")]
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "ServerAliyunModel 模型中未查到 env: %s 的对象" %(cmdb_obj.env)
            wslog_error().error("ServerAliyunModel 模型中未查到 env: %s 的对象,错误信息: %s" %(cmdb_obj.env,e.args))
            return JsonResponse(ret)

        try:
           cmdb_info = model_to_dict(cmdb_obj)
           del cmdb_info["offline_time"]
           cmdb_info["ips"] = [i["id"] for i in cmdb_obj.ips.values("id")]
           cmdb_info["ips_list"] = ips_list
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "CmdbModel 模型对象 %s 转为 dict 失败,请查看日志" %(cmdb_obj.name)
            wslog_error().error("CmdbModel 模型对象 %s 转为 dict 失败,错误信息: %s" %(cmdb_obj.name,e.args))
        else:
            ret["msg"] = "CmdbModel 模型对象 %s 转为 dict 成功" %(cmdb_obj.name)
            wslog_info().info("CmdbModel 模型对象 %s 转 dict 处理成功，可以提交给前端" %(cmdb_obj.name))
            ret["cmdb_info"] = cmdb_info

        return JsonResponse(ret)

    def post(self,request):
        ret = {"result":0,"msg":None}

        cid = request.POST.get("id")
        ret = GetCmdbObj(cid,ret)

        if ret["result"] == 1:
            return JsonResponse(ret)

        cmdb_obj = ret["msg"]

        cmdb_update_form = CmdbUpdateForm(request.POST)
        if not cmdb_update_form.is_valid():
            ret["result"] = 1
            ret["msg"] = json.dumps(json.loads(cmdb_update_form.errors.as_json(escape_html=False)),ensure_ascii=False)
            return JsonResponse(ret)
 
        try:
           cmdb_obj.env = cmdb_update_form.cleaned_data.get("env")
           cmdb_obj.type = cmdb_update_form.cleaned_data.get("type")
           cmdb_obj.way = cmdb_update_form.cleaned_data.get("way")
           cmdb_obj.describe = cmdb_update_form.cleaned_data.get("describe")
           cmdb_obj.path = cmdb_update_form.cleaned_data.get("path")
           cmdb_obj.log = cmdb_update_form.cleaned_data.get("log")
           cmdb_obj.ports = cmdb_update_form.cleaned_data.get("ports")
           cmdb_obj.script = cmdb_update_form.cleaned_data.get("script")
           cmdb_obj.status = cmdb_update_form.cleaned_data.get("status")
           cmdb_obj.save(update_fields=["env","type","way","describe","path","log","ports","script","status","last_update_time"])
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "CmdbModel 模型对象更新失败,请查看日志" %(cmdb_obj.name)
            wslog_error().error("CmdbModel 模型对象 %s 更新失败,错误信息: %s" %(cmdb_obj.name,e.args))
            return JsonResponse(ret)

        ips = request.POST.getlist("ips")
        ret = CmdbIpsUpdate(ips,cmdb_obj,ret)

        if ret["result"] == 0:
            ret["msg"] = "cmdb 模型对象: %s 更新成功" %(cmdb_obj.name)
            wslog_info().info("CmdbModel 模型对象: %s 添加成功" %(cmdb_obj.name))

        return JsonResponse(ret)


class CmdbInfoView(LoginRequiredMixin,View):

    def get(self,request):
        ret = {"result":0,"msg":None}        

        cid = request.GET.get('id')
        ret = GetCmdbObj(cid,ret)
        if ret["result"] == 1:
            return JsonResponse(ret)

        cmdb_obj = ret["msg"]

        try:
            cmdb_info = CmdbModel.objects.filter(id__exact=cid).values()[0]
            cmdb_info["env"] = cmdb_obj.get_env_display()
            cmdb_info["type"] = cmdb_obj.get_type_display()
            cmdb_info["way"] = cmdb_obj.get_way_display()
            cmdb_info["ips"] = "\n".join([ip["private_ip"] for ip in list(cmdb_obj.ips.values("private_ip"))])
            cmdb_info["ports"] = cmdb_obj.ports.replace(";","\n")
            if cmdb_info.get("online_time"):
                cmdb_info["online_time"] = utc_to_local(cmdb_info["online_time"]).strftime("%Y-%m-%d %X")
            if cmdb_info.get("offline_time"):
                cmdb_info["offline_time"] = utc_to_local(cmdb_info["offline_time"]).strftime("%Y-%m-%d %X")
            if cmdb_info.get("last_update_time"):
                cmdb_info["last_update_time"] = utc_to_local(cmdb_info["last_update_time"]).strftime("%Y-%m-%d %X")
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "CmdbModel 对象 %s 转为 dict 失败,请查看日志" %(cmdb_obj.name)
            wslog_error().error("CmdbModel 对象 %s 转为 dict 失败,错误信息: %s" %(cmdb_obj.name,e.args))
        else:
            wslog_info().info("获取 CmdbModel 对象 %s 信息成功" %(cmdb_obj.name))
            ret["msg"] = "CmdbModel 对象 %s 获取成功" %(cmdb_obj.name)
            ret["cmdb_info"] = cmdb_info
        
        
        return JsonResponse(ret)


class CmdbDeleteView(LoginRequiredMixin,View):

    def post(self,request):
        ret = {"result":0,"msg":None}
        cid = request.POST.get("id")

        ret = GetCmdbObj(cid,ret)
        if ret["result"] == 1:
            return JsonResponse(ret)

        cmdb_obj = ret["msg"]

        try:
            cmdb_obj.delete()
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "CmdbModel 删除对象 %s 失败，请查看日志" %(cmdb_obj.name)
            wslog_error().error("CmdbModel 删除 ID: %s 的对象失败,错误信息: %s" %(cid,e.args))
        else:
            ret["msg"] = "CmdbModel 删除对象 %s 成功" %(cmdb_obj.name)
            wslog_info().info("CmdbModel 删除对象 %s 成功" %(cmdb_obj.name))

        return JsonResponse(ret)
