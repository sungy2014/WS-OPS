from django.http import HttpResponse,JsonResponse
from django.views.generic import ListView,TemplateView,View
from resources.models import IDC 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import reverse
#from django.contrib.auth.mixins import PermissionRequiredMixin
from accounts.permission.permission_required_mixin import PermissionRequiredMixin
from resources.forms import IdcAddForm
import json

class IdcListView(PermissionRequiredMixin,ListView):
    permission_required = "resources.add_idc"
    permission_redirect_url = "user_list"
    template_name = "idc/idc_list.html"
    model = IDC
    paginate_by = 10
    ordering = "id"

class IdcAddView(TemplateView):
    template_name = 'idc/idc_add.html'

    def post(self,request):
        ret = {'result':0,'msg': None}
        idc_form = IdcAddForm(request.POST)
        if not idc_form.is_valid():
            ret['result'] = 1
            ret['msg'] = json.dumps(json.loads(idc_form.errors.as_json(escape_html=False)),ensure_ascii=False)
            return JsonResponse(ret)
        try:
            print("clean_data:",idc_form.cleaned_data)
            idc = IDC(**idc_form.cleaned_data)
            idc.save()
            ret['msg'] = "IDC %s 添加成功" %(idc_form.cleaned_data.get('cn_name'))
        except Exception as e:
            ret['result'] = 1
            ret['msg'] = e.args
        return JsonResponse(ret)

class IdcDeleteView(View):
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
