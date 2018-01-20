from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View,TemplateView,ListView
from accounts.permission.permission_required_mixin import PermissionRequiredMixin
from dashboard.utils.wslog import wslog_error,wslog_info
from workform.models import WorkFormModel,ProcessModel,ApprovalFormModel,WorkFormTypeModel
from opsweb.settings import MEDIA_ROOT
from datetime import datetime
import os
import json
from workform.forms import PubWorkFormAddForm
from django.db.models import Q
from django.contrib.auth.models import User,Group

''' 添加 发布工单 '''
class PubWorkFormAddView(LoginRequiredMixin,TemplateView):
    #permission_required = "resources.add_idc"
    #permission_redirect_url = "idc_list"
    
    template_name = "pub_workform_add.html"

    def get_context_data(self,**kwargs):
        context = super(PubWorkFormAddView,self).get_context_data(**kwargs)
        context["sql"] = dict(WorkFormModel.SQL_CHOICES)
        context["level"] = dict(WorkFormModel.LEVEL_CHOICES)
        return context

    def get_approver_can(self,user_obj,applicant_require,ret):

        ''' 针对审核要求是组的情况，写了下面这个字典，主要是为了简化代码量'''
        applicant_require_dict = {"2":"qa","3":"ops","6":"ws-trade","7":"ws-item","8":"ws-user"}

        user_obj_list = []

        ''' 对审核要求为组的情况,做了统一处理,也就简化了代码量'''
        if applicant_require in ["2","3","6","7","8"] :
            try:
                user_obj_list = list(Group.objects.get(name__exact=applicant_require_dict.get(applicant_require,"ops")).user_set.exclude(id__exact=user_obj.id))
            except Exception as e:
                ret["result"] = 1
                ret["msg"] = "获取 %s 组内可以审核的用户对象失败,请联系运维人员" %(applicant_require_dict.get(applicant_require,"ops"))
                wslog_error().error("获取 %s 组内可以审核的用户对象失败,错误信息: %s" %(applicant_require_dict.get(applicant_require,"ops"),e.args))
            else:
                ret["user_obj_list"] = user_obj_list

        elif applicant_require == '1' :
            try:
                for group_obj in user_obj.groups.all() :
                    user_obj_list += list(group_obj.user_set.exclude(id__excat=user_obj.id))
            except Exception as e:
                ret["result"] = 1
                ret["msg"] = "获取可以审核的用户对象失败,请联系运维人员"
                wslog_error().error("获取可以审核的用户对象失败,错误信息: %s" %(e.args))
            else: 
                ret["user_obj_list"] = user_obj_list

        elif applicant_require == "4" :
            user_obj_list.append(user_obj)
            ret["user_obj_list"] = user_obj_list

        else:
            ret["result"] = 1
            ret["msg"] = "此流程步骤所需的审核组或用户: %s 未配置,请联系运维进行配置" %(applicant_require)
            wslog_error().error("此流程步骤未配置相应的审核组或用户: %s,请进行配置" %(applicant_require))

        return ret

    def post(self,request):
        ret = {"result":0,"msg":"success"}
        user_cn_name = request.user.userextend.cn_name

        pub_workform_add_form = PubWorkFormAddForm(request.POST)
        if not pub_workform_add_form.is_valid():
            ret["result"] = 1
            ret["msg"] = json.dumps(json.loads(pub_workform_add_form.errors.as_json(escape_html=False)),ensure_ascii=False)
            return JsonResponse(ret) 

        workform_type = request.POST.get("type",None)
        if not workform_type:
            ret["result"] = 1
            ret["msg"] = "工单必须选择一个类型"
            return JsonResponse(ret)

        try:
            wft_obj = WorkFormTypeModel.objects.get(name__exact=workform_type)
        except WorkFormTypeModel.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "该工单类型:'%s' 在模型 WorkFormTypeModel 中不存在,请联系运维人员" %(workform_type)
            wslog_error().error("用户: %s 添加工单,该工单类型:'%s' 在模型 WorkFormTypeModel 中不存在,请检查" %(user_cn_name,workform_type))
            return JsonResponse(ret)
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "该工单类型:'%s' 在模型 WorkFormTypeModel 中查询异常,请联系运维人员" %(workform_type)
            wslog_error().error("用户: %s 添加工单,工单类型:'%s' 在模型 WorkFormTypeModel 中查询异常,错误信息: %s" %(user_cn_name,workform_type,e.args))
            return JsonResponse(ret) 
        else:
            process_step_list = wft_obj.process_step_id.split(" -> ")

        try:
            pub_workform_obj = WorkFormModel(**pub_workform_add_form.cleaned_data)
            pub_workform_obj.applicant = request.user.userextend.cn_name
            pub_workform_obj.type = wft_obj
            pub_workform_obj.save()
        except Exception as e:
            ret["result"] = 1
            print("e.args:",e.args)
            ret["msg"] = "WorkFormModel 模型对象保存失败,错误信息: %s" %(e.args)
            wslog_error().error("用户: %s 添加 WorkFormModel 模型对象 '%s' 保存失败,错误信息: %s" %(user_cn_name,pub_workform_add_form.cleaned_data.get("title"),e.args))
            return JsonResponse(ret)

        for process_step in process_step_list:
            try:
                process_obj = ProcessModel.objects.get(step_id__exact=process_step)
            except ProcessModel.DoesNotExist:
                ret["result"] = 1
                ret["msg"] = "ProcessModel 模型不存在 step_id 为 %s 的对象,请联系运维人员" %(process_step)
                wslog_error().error("用户: %s 添加工单: '%s' 中 ProcessModel 模型不存在 step_id 为 %s 的对象" %(user_cn_name,pub_workform_obj.title,process_step))
                break
            except Exception as e:
                ret["result"] = 1
                ret["msg"] = "ProcessModel 模型查找 step_id 为 %s 的对象发生异常,请联系运维人员" %(process_step)
                wslog_error().error("用户: %s 添加工单: '%s' 中 ProcessModel 模型查找 step_id 为 %s 的对象异常，错误信息: %s" %(user_cn_name,pub_workform_obj.title,process_step,e.args))
                break

            try:
                pub_workform_obj.process.add(process_obj) 
            except Exception as e:
                ret["result"] = 1
                ret["msg"] = "WorkFormModel 模型 多对多关联 ProcessModel 模型对象 %s 失败,请联系运维人员" %(process_step)
                wslog_error().error("用户: %s 添加工单: '%s' 中 WorkFormModel 模型 多对多关联 ProcessModel 模型对象 %s 失败,错误信息: %s" %(user_cn_name,pub_workform_obj.title,process_step,e.args))
                break

            applicant_require = process_obj.applicant_require

            ret = self.get_approver_can(request.user,applicant_require,ret)

            if ret["result"] == 1:
                break

            af_obj = ApprovalFormModel()
            try:
                af_obj.workform = pub_workform_obj
                af_obj.process = process_obj
                af_obj.save()
            except Exception as e:
                ret["result"] = 1
                del ret["user_obj_list"]
                ret["msg"] = "ApprovalFormModel 模型保存对象失败,请联系运维人员"
                wslog_error().error("用户: %s 添加工单: '%s' 中 ApprovalFormModel 模型保存对象失败,错误信息: %s" %(user_cn_name,pub_workform_obj.title,e.args))
                break
            else:
                af_obj.approver_can.set(ret["user_obj_list"])
                del ret["user_obj_list"]

        if ret["result"] == 0:
            ret["msg"] = "发布工单: '%s' 创建成功" %(pub_workform_add_form.cleaned_data.get("title"))
            wslog_info().info("用户: %s 发布工单: '%s' 创建成功" %(user_cn_name,pub_workform_obj.title))

        return JsonResponse(ret)


class WorkFormListView(ListView):
    template_name = "workform_list.html"
    model = WorkFormModel
    paginate_by =10
    ordering = '-id'
    page_total = 11

    def get_context_data(self,**kwargs):
        context = super(WorkFormListView,self).get_context_data(**kwargs)
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
        queryset = super(WorkFormListView,self).get_queryset()

        search_name = self.request.GET.get('search',None)
        if search_name:
            queryset = queryset.filter(Q(title__icontains=search_name)|Q(detail__icontains=search_name)|Q(module_name__icontains=search_name))
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

class MyWorkFormListView(ListView):
    template_name = "my_workform_list.html"
    model = WorkFormModel
    paginate_by =10
    ordering = '-id'
    page_total = 11

    def get_context_data(self,**kwargs):
        context = super(MyWorkFormListView,self).get_context_data(**kwargs)
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
        queryset = super(MyWorkFormListView,self).get_queryset()
        queryset = WorkFormModel.objects.filter(applicant__exact=self.request.user)

        search_name = self.request.GET.get('search',None)
        if search_name:
            queryset = queryset.filter(Q(title__icontains=search_name)|Q(detail__icontains=search_name)|Q(module_name__icontains=search_name))
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


''' 发布工单中 SQL附件的上传 '''
class PubWorkFormUploadView(LoginRequiredMixin,View):
    allow_file_type=set(['txt','sql'])
    upload_dir = MEDIA_ROOT + 'pub/'
    max_file_size = 10 * 1024 * 1024

    def post(self,request):
        ret = {"result":0,"msg":None}
        files = request.FILES.getlist('files[]')
        for file in files:
            filename = file.name
            filesize = file.size
            if '.' not in filename or  filename.rsplit('.',1)[1] not in self.allow_file_type:
                ret["result"] = 1
                ret["msg"] = "The file '%s' format is not allow" %(filename)
                return JsonResponse(ret)
            if filesize >= self.max_file_size:
                ret["result"] = 1
                ret["msg"] = "The file '%s' size %s is more than 10Mb" %(filename,filesize)

            file_upload_time = datetime.now().strftime("%Y%m%d%H%M%S")
            file_store_name = filename.rsplit('.',1)[0] + '_' + file_upload_time + '.' + filename.rsplit('.',1)[1]
            file_url = reverse("pub_workform_upload") + file_store_name
            store_dir_name = self.upload_dir + file_store_name
            try:
                with open(store_dir_name, 'wb+') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
            except Exception as e:
                ret["result"] = 1
                ret["msg"] = "文件 %s 保存失败,错误信息: %s,请联系运维人员" %(filename,e.args)
            else:
                ret["files"] = [{"name": file_store_name}]
                ret["file_url"] = file_url

            return JsonResponse(ret)

''' 发布工单中 SQL 附件的预览'''
class PubWorkFormUploadFilePreviewView(LoginRequiredMixin,View):

    def download_file(self,filename):
        with open(filename,'rb') as f:
            c = f.read()
        return c.decode('utf-8').replace('\n','</br>')

    def get(self,request,**kwargs):
        filename = kwargs.get("filename")
        filename_path = MEDIA_ROOT + 'pub/' + filename

        if not os.path.exists(filename_path):
            return HttpResponse("该文件 %s 不存在或已被删除" %(filename_path))

        response=StreamingHttpResponse(self.download_file(filename_path))
        #response['Content-Type']="application/octet-stream" 
        #response['Content-Disposition']="attachment;filename='%s'" %(filename)
        return response   

