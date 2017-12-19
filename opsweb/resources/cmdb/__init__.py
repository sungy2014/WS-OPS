from django.views.generic import View,TemplateView,ListView
from django.http import JsonResponse
from resources.models import CmdbModel,ServerAliyunModel
from resources.forms import CmdbAddForm
from dashboard.utils.wslog import wslog_error,wslog_info


class CmdbListView(ListView):
    template_name = "cmdb/cmdb_list.html"
    model = CmdbModel
    paginate_by = 10


class CmdbAddView(TemplateView):
    template_name = "cmdb/cmdb_add.html"

    def get_context_data(self,**kwargs):
        context = super(CmdbAddView,self).get_context_data(**kwargs)
        context["server_ips"] = [ {"id":i["id"],"private_ip":i['private_ip']} for i in ServerAliyunModel.objects.values("id","private_ip")]
        context["type"] = dict(CmdbModel.TYPE_CHOICES)
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
            cmdb_obj.save()
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "CmdbModel 模型对象: %s 添加失败,请查看日志" %(cmdb_add_form.cleaned_data.get("name"))
            wslog_error().error("CmdbModel 模型对象: %s 添加失败，错误信息: %s" %(cmdb_add_form.cleaned_data.get("name"),e.args))
            return JsonResponse(ret)

        ips = request.POST.getlist("ips")
        
        if not ips:
            ret["result"] = 1
            ret["msg"] = "请至少选择一个IP"
            return JsonResponse(ret)

        try:
            server_obj_list = [ServerAliyunModel.objects.get(id__exact=sid) for sid in ips]
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "ServerAliyunModel 查询对象失败，请刷新并重新选择IP地址"
            wslog_error().error("ServerAliyunModel 查询对象地址失败" %(e.args))
            return JsonResponse(ret)

        try:
            cmdb_obj.ips.set(server_obj_list)
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "CmdbModel模型对象: %s 关联 ServerAliyunModel 失败,请查看日志" %(cmdb_add_form.cleaned_data.get("name"))
            wslog_error().error("CmdbModel 模型对象: %s 关联 ServerAliyunModel 失败,错误信息: %s" %(cmdb_add_form.cleaned_data.get("name"),e.args))
        else:
            ret["msg"] = "cmdb 模型对象: %s 添加成功" %(cmdb_add_form.cleaned_data.get("name"))
            wslog_info().info("CmdbModel 模型对象: %s 添加成功" %(cmdb_add_form.cleaned_data.get("name")))
        
        return JsonResponse(ret)

class CmdbChangeView(View):
    def get(self,request):
        ret = {"result":0,"msg":None}
        return JsonResponse(ret)

class CmdbDeleteView(View):
    def get(self,request):
        ret = {"result":0,"msg":None}
        return JsonResponse(ret)
