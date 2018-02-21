from django.http import JsonResponse,HttpResponse
from django.views.generic import TemplateView,ListView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from accounts.permission.permission_required_mixin import PermissionRequiredMixin
import json
from django.db.models import Q,F
from datetime import *
from dashboard.utils.utc_to_local import utc_to_local
from dashboard.utils.wslog import wslog_error,wslog_info
from workform.models import WorkFormTypeModel,ProcessModel
from workform.forms import WorkFormProcessAddForm,WorkFormProcessChangeForm

''' 流程列表 '''
class WorkFormProcessListView(LoginRequiredMixin,ListView):
    template_name = 'workform_process_list.html'
    paginate_by = 10
    model = ProcessModel
    ordering = 'id'
    page_total = 11

    def get_context_data(self,**kwargs):
        context = super(WorkFormProcessListView,self).get_context_data(**kwargs)
        context['page_range'] = self.get_page_range(context['page_obj'])
        context["approval_require_list"] = dict(ProcessModel.APPLICANT_CHOICES) 
        search_data = self.request.GET.copy()
        try:
            search_data.pop('page')
        except:
            pass

        if search_data:
            context['search_uri'] = '&' + search_data.urlencode()
        else:
            context['search_uri'] = '' 
        context.update(search_data.dict())
        return context

    def get_queryset(self):
        queryset = super(WorkFormProcessListView,self).get_queryset()

        search_name = self.request.GET.get('search',None)
        if search_name:
            queryset = queryset.filter(step__icontains=search_name)
        return queryset
    
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

''' 添加流程 step '''
class WorkFormProcessAddView(LoginRequiredMixin,TemplateView):

    def post(self,request):
        ret = {"result":0}
        
        workform_process_form = WorkFormProcessAddForm(request.POST) 

        if not workform_process_form.is_valid():
            ret["result"] = 1
            error_msg = json.loads(workform_process_form.errors.as_json(escape_html=False)) 
            ret["msg"] = '\n'.join([ i["message"] for v in error_msg.values() for i in v ])
            return JsonResponse(ret)
        
        try:
            pm_obj = ProcessModel(**workform_process_form.cleaned_data)
            step_id_list = ProcessModel.objects.values_list("step_id").order_by("-id")
            pm_obj.step_id = step_id_list[0][0] + 10 if step_id_list else 10
            pm_obj.save()
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "流程Step: '%s' 添加失败,请查看日志" %(workform_process_form.cleaned_data.get("step"))
            wslog_error().error("流程step: '%s' 添加失败,错误信息: %s" %(workform_process_form.cleaned_data.get("step"),e.args))
            return JsonResponse(ret)
        else:
            ret["msg"] = "流程step: '%s' 添加成功" %(workform_process_form.cleaned_data.get("step"))

        return JsonResponse(ret)

''' 删除流程 step '''
class WorkFormProcessDeleteView(LoginRequiredMixin,View):
    def get(self,request):
        ret = {"result":0}
        pm_id = request.GET.get("id")

        try:
            pm_obj = ProcessModel.objects.get(id__exact=pm_id)
            pm_obj.delete()
        except ProcessModel.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "ProcessModel 模型不存在 id: %s 的对象,请刷新重试" %(pm_id)
            return JsonResponse(ret)
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "ProcessModel 模型删除 id: %s 的对象失败,请查看日志" %(pm_id)
            wslog_error().error("ProcessModel 模型删除 id %s 的对象失败,错误信息: %s" %(pm_id,e.args))
            return JsonResponse(ret) 
        else:
            ret["msg"] = "ProcessModel 模型删除 id: %s 的对象成功" %(pm_id) 
        
        return JsonResponse(ret)

''' 修改流程 step '''
class WorkFormProcessChangeView(LoginRequiredMixin,View):
    def get(self,request):
        ret = {"result":0}
        pm_id = request.GET.get("id")
        try:
            pm_obj = ProcessModel.objects.get(id__exact=pm_id)
        except ProcessModel.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "ProcessModel 模型不存在 id: %s 的对象,请刷新重试" %(pm_id)
            return JsonResponse(ret)
        else:
            ret["pm_info"] = model_to_dict(pm_obj)

        return JsonResponse(ret)

    def post(self,request):
        ret = {"result":0}
        pm_id = request.POST.get("id")
        try:
            pm_obj = ProcessModel.objects.get(id__exact=pm_id)
        except ProcessModel.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "ProcessModel 模型不存在 id: %s 的对象,请刷新重试" %(pm_id)
            return JsonResponse(ret)
             
        workform_process_change_form = WorkFormProcessChangeForm(request.POST)

        if not workform_process_change_form.is_valid():
            ret["result"] = 1
            error_msg = json.loads(workform_process_change_form.errors.as_json(escape_html=False))
            ret["msg"] = '\n'.join([ i["message"] for v in error_msg.values() for i in v ])
            print("error:",ret["msg"])
            return JsonResponse(ret)
        try:
            pm_obj.approval_require = workform_process_change_form.cleaned_data.get("approval_require")
            pm_obj.save(update_fields=["approval_require"])
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "ProcessModel 模型更新对象 id: %s 失败,请查看日志" %(pm_obj.step)
            wslog_error().error("ProcessModel 模型更新对象 id: %s 失败,错误信息: %s " %(pm_id,e.args))
        else:
            ret["msg"] = "ProcessModel 模型更新对象 '%s' 成功" %(pm_obj.step)

        return JsonResponse(ret)
        
