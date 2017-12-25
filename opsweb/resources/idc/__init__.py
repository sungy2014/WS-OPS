from django.http import HttpResponse,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,TemplateView,View
from resources.models import IDC 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import reverse
#from django.contrib.auth.mixins import PermissionRequiredMixin
from accounts.permission.permission_required_mixin import PermissionRequiredMixin
from resources.forms import IdcAddForm,IdcChangeForm
import json
from django.forms.models import model_to_dict
from dashboard.utils.wslog import wslog_error,wslog_info


class IdcListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = "resources.add_idc"
    permission_redirect_url = "users_list"
    template_name = "idc/idc_list.html"
    model = IDC
    paginate_by = 10
    ordering = "id"

class IdcAddView(LoginRequiredMixin,TemplateView):
    template_name = 'idc/idc_add.html'

    def post(self,request):
        ret = {'result':0,'msg': None}
        idc_form = IdcAddForm(request.POST)
        if not idc_form.is_valid():
            ret['result'] = 1
            ret['msg'] = json.dumps(json.loads(idc_form.errors.as_json(escape_html=False)),ensure_ascii=False)
            return JsonResponse(ret)
        try:
            idc = IDC(**idc_form.cleaned_data)
            idc.save()
            ret['msg'] = "IDC %s 添加成功" %(idc_form.cleaned_data.get('cn_name'))
        except Exception as e:
            ret['result'] = 1
            ret['msg'] = e.args
        return JsonResponse(ret)

class IdcChangeView(LoginRequiredMixin,View):
    def get(self,request):
        
        ret = {"result":0,"msg":None}
        idc_id = request.GET.get("id",0)

        try:
            idc_obj = IDC.objects.get(id__exact=idc_id)
        except IDC.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "IDC id: %s 不存在,请刷新重试" %(idc_id)
            wslog_error().error("IDC 模型对象id: %s 不存在" %(idc_id))
            return JsonResponse(ret)
        try:
            idc_info = model_to_dict(idc_obj)
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "IDC 模型对象转dict 失败,请查看日志"
            wslog_error().error("IDC 模型对象id: %s 转dict 失败,错误信息: %s" %(idc_id,e.args))
        else:
            ret["idc_info"] = idc_info
            wslog_info().info("IDC 模型对象id: %s 查询成功并返回给前端" %(idc_id))

        return JsonResponse(ret)

    def post(self,request):
        
        ret = {"result":0,"msg":None}
        idc_id = request.POST.get("id",0)
        idc_form = IdcChangeForm(request.POST)

        if not idc_form.is_valid():
            ret['result'] = 1
            ret['msg'] = json.dumps(json.loads(idc_form.errors.as_json(escape_html=False)),ensure_ascii=False)
            return JsonResponse(ret)

        try:
            idc_obj = IDC.objects.get(id__exact=idc_id)
        except IDC.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "IDC id: %s 不存在,请刷新重试" %(idc_id)
            wslog_error().error("IDC 模型对象id: %s 不存在" %(idc_id))
            return JsonResponse(ret)
        
        idc_change_info = idc_form.cleaned_data    

        try:
            idc_obj.user = idc_change_info.get("user")
            idc_obj.email = idc_change_info.get("email")
            idc_obj.phone = idc_change_info.get("phone")
            idc_obj.address = idc_change_info.get("address")
            idc_obj.save(update_fields=["user","email","phone","address","last_update_time"])
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "IDC: %s 修改信息保存失败,请查看日志" %(idc_obj.cn_name)
            wslog_error().error("IDC: id-%s 保存修改信息失败,错误信息: %s" %(idc_id,e.args))
        else:
            ret["msg"] = "IDC: %s 更改信息成功" %(idc_obj.cn_name)
            wslog_info().info("IDC: id-%s 更改信息成功" %(idc_id))
        
        return JsonResponse(ret)

class IdcDeleteView(LoginRequiredMixin,View):
    def get(self,request):
        idc_id = request.GET.get('id',None)
        ret = {'result':0,'msg': None}
        try:
            idc = IDC.objects.get(id=idc_id)
            idc.delete()
            ret['msg'] = "%s 删除成功" %(idc.cn_name)
        except IDC.DoesNotExist:
            ret['result'] = 1
            ret['msg'] = "删除失败,获取不到 IDC id"
            return JsonResponse(ret)
        return JsonResponse(ret)
