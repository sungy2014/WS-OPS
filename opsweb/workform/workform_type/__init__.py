from django.http import JsonResponse,HttpResponse
from django.views.generic import TemplateView,ListView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from accounts.permission.permission_required_mixin import PermissionRequiredMixin
import json
from django.db.models import Q
from datetime import *
from dashboard.utils.utc_to_local import utc_to_local
from dashboard.utils.wslog import wslog_error,wslog_info
from workform.models import WorkFormTypeModel,ProcessModel
from workform.forms import WorkFormTypeAddForm,WorkFormTypeChangeForm


''' 工单类型列表 '''
class WorkFormTypeListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = "workform.view_workformtypemodel"
    permission_redirect_url = "workform_list"

    template_name = 'workform_type_list.html'
    paginate_by = 10
    model = WorkFormTypeModel
    ordering = 'id'
    page_total = 11

    def get_context_data(self,**kwargs):
        context = super(WorkFormTypeListView,self).get_context_data(**kwargs)
        context['page_range'] = self.get_page_range(context['page_obj'])
        context["process_step_list"] = list(ProcessModel.objects.values("step","step_id"))
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
        queryset = super(WorkFormTypeListView,self).get_queryset()

        search_name = self.request.GET.get('search',None)
        if search_name:
            queryset = queryset.filter(Q(name__icontains=search_name)|Q(cn_name__icontains=search_name))
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

''' 添加工单类型 '''
class WorkFormTypeAddView(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    permission_required = "workform.add_workformtypemodel"
    permission_redirect_url = "workform_list"

    template_name = "workform_type_add.html"
    
    def get_context_data(self):
        context = super(WorkFormTypeAddView,self).get_context_data()
        context["process_step_list"] = list(ProcessModel.objects.values("step","step_id"))
        return context


    def post(self,request):
        ret = {"result":0}
        
        ## ajax 请求的权限验证
        if not request.user.has_perm(self.permission_required):
            ret["result"] = 1
            ret["msg"] = "Sorry,你没有'添加工单类型'的权限,请联系运维!"
            return JsonResponse(ret) 

        workform_type_form = WorkFormTypeAddForm(request.POST) 

        if not workform_type_form.is_valid():
            ret["result"] = 1
            error_msg = json.loads(workform_type_form.errors.as_json(escape_html=False)) 
            ret["msg"] = '\n'.join([ i["message"] for v in error_msg.values() for i in v ])
            return JsonResponse(ret)
        
        try:
            wft_obj = WorkFormTypeModel(**workform_type_form.cleaned_data)
            wft_obj.save()
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "工单类型: '%s' 添加失败" %(workform_type_form.cleaned_data.get("cn_name"))
            wslog_error().error("工单类型: '%s' 添加失败,错误信息: %s" %(workform_type_form.cleaned_data.get("cn_name"),e.args))
            return JsonResponse(ret)
        else:
            ret["msg"] = "工单类型: '%s' 添加成功" %(workform_type_form.cleaned_data.get("cn_name"))

        return JsonResponse(ret)

''' 删除工单类型 '''
class WorkFormTypeDeleteView(LoginRequiredMixin,View):
    permission_required = "workform.delete_workformtypemodel"

    def get(self,request):
        ret = {"result":0}

        ## ajax 请求的权限验证
        if not request.user.has_perm(self.permission_required):
            ret["result"] = 1
            ret["msg"] = "Sorry,你没有'删除工单类型'的权限,请联系运维!"
            return JsonResponse(ret)

        wft_id = request.GET.get("id")

        try:
            wft_obj = WorkFormTypeModel.objects.get(id__exact=wft_id)
            wft_obj.delete()
        except WorkFormTypeModel.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "WorkFormTypeModel 模型不存在 id: %s 的对象,请刷新重试" %(wft_id)
            return JsonResponse(ret)
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "WorkFormTypeModel 模型删除 id: %s 的对象失败,请查看日志" %(wft_id)
            wslog_error().error("WorkFormTypeModel 模型删除 id %s 的对象失败,错误信息: %s" %(wft_id,e.args))
            return JsonResponse(ret) 
        else:
            ret["msg"] = "WorkFormTypeModel 模型删除 id: %s 的对象成功" %(wft_id) 
        
        return JsonResponse(ret)

''' 修改工单类型 '''
class WorkFormTypeChangeView(LoginRequiredMixin,View):
    permission_required = "workform.change_workformtypemodel"

    def perm_check(self,request,ret):
        ## ajax 请求的权限验证
        if not request.user.has_perm(self.permission_required):
            ret["result"] = 1
            ret["msg"] = "Sorry,你没有'修改工单类型'的权限,请联系运维!"
            return JsonResponse(ret)

    def get(self,request):
        ret = {"result":0}

        self.perm_check(request,ret)

        wft_id = request.GET.get("id")
        try:
            wft_obj = WorkFormTypeModel.objects.get(id__exact=wft_id)
        except WorkFormTypeModel.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "WorkFormTypeModel 模型不存在 id: %s 的对象,请刷新重试" %(wft_id)
            return JsonResponse(ret)
        else:
            ret["wft_info"] = model_to_dict(wft_obj)
            ret["wft_info"]["process_step_id"] = ret["wft_info"]["process_step_id"].split(" -> ")

        return JsonResponse(ret)

    def post(self,request):
        ret = {"result":0}
    
        self.perm_check(request,ret)    

        wft_id = request.POST.get("id")
        wft_cn_name = request.POST.get("cn_name")
        try:
            wft_obj = WorkFormTypeModel.objects.get(id__exact=wft_id)
        except WorkFormTypeModel.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "WorkFormTypeModel 模型不存在 id: %s 的对象,请刷新重试" %(wft_id)
            return JsonResponse(ret)

        if WorkFormTypeModel.objects.exclude(id__exact=wft_id).filter(cn_name__exact=wft_cn_name):
            ret["result"] = 1
            ret["msg"] = "WorkFormTypeModel 模型中其他的对象已使用此中文名"
            return JsonResponse(ret)
             
        workform_type_change_form = WorkFormTypeChangeForm(request.POST)

        if not workform_type_change_form.is_valid():
            ret["result"] = 1
            error_msg = json.loads(workform_type_change_form.errors.as_json(escape_html=False))
            ret["msg"] = '\n'.join([ i["message"] for v in error_msg.values() for i in v ])
            print("error:",ret["msg"])
            return JsonResponse(ret)
        try:
            wft_obj.cn_name = request.POST.get("cn_name")
            wft_obj.process_step_id = workform_type_change_form.cleaned_data.get("process_step_id")
            wft_obj.save(update_fields=["cn_name","process_step_id"])
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "WorkFormTypeModel 模型更新对象 id: %s 失败,请查看日志" %(wft_id)
            wslog_error().error("WorkFormTypeModel 模型更新对象 id: %s 失败,错误信息: %s " %(wft_id,e.args))
        else:
            ret["msg"] = "WorkFormTypeModel 模型更新对象 '%s' 成功" %(wft_obj.cn_name)

        return JsonResponse(ret)
        
