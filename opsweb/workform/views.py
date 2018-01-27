from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View,TemplateView,ListView
from accounts.permission.permission_required_mixin import PermissionRequiredMixin
from dashboard.utils.wslog import wslog_error,wslog_info
from workform.models import WorkFormModel,ProcessModel,ApprovalFormModel,WorkFormTypeModel,WorkFormBaseModel
from opsweb.settings import MEDIA_ROOT
from datetime import datetime
import os
import json
from workform.forms import PubWorkFormAddForm,WorkFormApprovalForm
from django.db.models import Q
from django.contrib.auth.models import User,Group
from dashboard.utils.utc_to_local import utc_to_local

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

    def get_approver_can(self,user_obj,approval_require,ret):

        ''' 针对审核要求是组的情况，写了下面这个字典，主要是为了简化代码量'''
        approval_require_dict = {"2":"qa","3":"ops","6":"ws-trade","7":"ws-item","8":"ws-user"}

        user_obj_list = []

        ''' 对审核要求为组的情况,做了统一处理,也就简化了代码量'''
        if approval_require in ["2","3","6","7","8"] :
            try:
                user_obj_list = list(Group.objects.get(name__exact=approval_require_dict.get(approval_require,"ops")).user_set.exclude(id__exact=user_obj.id))
            except Exception as e:
                ret["result"] = 1
                ret["msg"] = "获取 %s 组内可以审核的用户对象失败,请联系运维人员" %(approval_require_dict.get(approval_require,"ops"))
                wslog_error().error("获取 %s 组内可以审核的用户对象失败,错误信息: %s" %(approval_require_dict.get(approval_require,"ops"),e.args))
            else:
                ret["user_obj_list"] = user_obj_list

        elif approval_require == '1' :
            try:
                for group_obj in user_obj.groups.all() :
                    user_obj_list += list(group_obj.user_set.exclude(id__exact=user_obj.id))
            except Exception as e:
                ret["result"] = 1
                ret["msg"] = "获取可以审核的用户对象失败,请联系运维人员"
                wslog_error().error("获取可以审核的用户对象失败,错误信息: %s" %(e.args))
            else: 
                ret["user_obj_list"] = user_obj_list

        elif approval_require == "4" or approval_require == "9":
            user_obj_list.append(user_obj)
            ret["user_obj_list"] = user_obj_list
 
        else:
            ret["result"] = 1
            ret["msg"] = "此流程步骤所需的审核组或用户: %s 未配置,请联系运维进行配置" %(approval_require)
            wslog_error().error("此流程步骤: %s 未配置相应的审核组或用户,请进行配置" %(approval_require))

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
            p_obj = ProcessModel.objects.get(step_id__exact=process_step_list[0])
            pub_workform_obj = WorkFormModel(**pub_workform_add_form.cleaned_data)
            pub_workform_obj.applicant = request.user
            pub_workform_obj.type = wft_obj
            pub_workform_obj.process_step = p_obj
            pub_workform_obj.save()
        except Exception as e:
            ret["result"] = 1
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
                pub_workform_obj.delete()
                break
            except Exception as e:
                ret["result"] = 1
                ret["msg"] = "ProcessModel 模型查找 step_id 为 %s 的对象发生异常,请联系运维人员" %(process_step)
                wslog_error().error("用户: %s 添加工单: '%s' 中 ProcessModel 模型查找 step_id 为 %s 的对象异常，错误信息: %s" %(user_cn_name,pub_workform_obj.title,process_step,e.args))
                pub_workform_obj.delete()
                break

            approval_require = process_obj.approval_require

            ret = self.get_approver_can(request.user,approval_require,ret)

            if ret["result"] == 1:
                pub_workform_obj.delete()
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
                pub_workform_obj.delete()
                break

            if ret["user_obj_list"]:
                af_obj.approver_can.set(ret["user_obj_list"])
                del ret["user_obj_list"]
            else:
                ret["result"] = 1
                ret["msg"] = "该流程步骤 %s 未查到可审核的用户对象列表,请联系运维人员" %(process_step)
                pub_workform_obj.delete()
                break

        if ret["result"] == 1:
            return JsonResponse(ret)
        
        ''' 
            根据ApprovalFormModel中的approver_can字段关联的User对象,来生成WorkFormModel中 approver_can字段 与User对象的多对多关系,
            相当于 复制了ApprovalFormModel中的approver_can字段
        '''
        try:
            pub_workform_obj.approver_can.set(pub_workform_obj.approvalformmodel_set.get(process_id__exact=pub_workform_obj.process_step_id).approver_can.all())
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "根据模型ApprovalFormModel的字段approver_can来生成模型WorkFormModel字段approver_can与User多对多关系失败"
            wslog_error().error("根据模型ApprovalFormModel的字段approver_can来生成模型WorkFormModel字段approver_can与User多对多关系失败")
            pub_workform_obj.delete()
        else:
            ret["msg"] = "发布工单: '%s' 创建成功" %(pub_workform_add_form.cleaned_data.get("title"))
            wslog_info().info("用户: %s 发布工单: '%s' 创建成功" %(user_cn_name,pub_workform_obj.title))

        return JsonResponse(ret)

''' 工单列表 '''
class WorkFormListView(LoginRequiredMixin,ListView):
    template_name = "workform_list.html"
    model = WorkFormModel
    paginate_by =10
    ordering = '-id'
    page_total = 11

    def get_context_data(self,**kwargs):
        context = super(WorkFormListView,self).get_context_data(**kwargs)
        context['page_range'] = self.get_page_range(context['page_obj'])
        context['level_range'] = range(0,len(WorkFormBaseModel.LEVEL_CHOICES))
        context['approval_result'] = dict(ApprovalFormModel.RESULT_CHOICES)
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

''' 我的工单列表: 我发出的工单和我待审核的工单 '''
class MyWorkFormListView(WorkFormListView):
    template_name = "my_workform_list.html"
    ordering = "-id"

    def get_queryset(self):
        queryset = super(MyWorkFormListView,self).get_queryset()
        queryset = WorkFormModel.objects.filter(Q(applicant__username__exact=self.request.user.username)|Q(approver_can__username__exact=self.request.user.username)).distinct()

        search_name = self.request.GET.get('search',None)
        if search_name:
            queryset = queryset.filter(Q(title__icontains=search_name)|Q(detail__icontains=search_name)|Q(module_name__icontains=search_name)).distinct()
        return queryset

''' 我审核过的工单列表 '''
class MyApprovaledWorkFormListView(LoginRequiredMixin,View):
    def get(self,request):
        ret = {'result':0}

        try:
            my_approvaled_workform_list = list(WorkFormModel.objects.filter(approvalformmodel__approver__username__exact=request.user.username).distinct().values())
        except Exception as e:
            ret["result"] = 1
            wslog_error().error("生成当前用户审核过的工单列表失败,错误信息: %s" %(e.args))
        else:
            ret["approvaled_workform_list"] = my_approvaled_workform_list

        return JsonResponse(ret)

''' 审批工单 '''
class ApprovalWorkFormView(LoginRequiredMixin,View):
    def get(self,request):
        ret = {"result":0}

        wf_id = request.GET.get("id")
        process_step_id = request.GET.get("process_id")

        try:
            wf_obj = WorkFormModel.objects.get(id__exact=wf_id)
        except WorkFormModel.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "WorkFormModel 模型不存在 id: %s 的对象,请刷新重试..." %(wf_id)
            wslog_error().error("WorkFormModel 模型不存在 id: %s 的对象" %(wf_id))
            return JsonResponse(ret)

        try:
            wf_info = WorkFormModel.objects.filter(id__exact=wf_id).values("id","title","detail","applicant","module_name")[0]
            wf_info["level"] = wf_obj.get_level_display()
            wf_info["process"] = wf_obj.process_step.step
            wf_info["type"] = wf_obj.type.cn_name
            wf_info["applicant"] = wf_obj.applicant.userextend.cn_name
            wf_info["status"] = wf_obj.get_status_display()
            wf_info["process_step_id"] = process_step_id
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "WorkFormModel 模型 id: %s 的对象转 dict 失败,请查看日志..." %(wf_id)
            wslog_error().error("WorkFormModel 模型 id: %s 的对象转 dict 失败,错误信息: %s" %(wf_id,e.args))
        else:
            wslog_info().info("WorkFormModel 模型 id: %s 的对象转 dict 成功,查询该对象的详情成功" %(wf_id))
            ret["wf_info"] = wf_info
        return JsonResponse(ret)

    def post(self,request):
        ret = {"result":0}

        wf_id = request.POST.get("id")
        process_step_id = request.POST.get("process_step_id")

        workform_approval_form = WorkFormApprovalForm(request.POST)

        if not workform_approval_form.is_valid():
            ret["result"] = 1
            ret["msg"] = json.dumps(json.loads(workform_approval_form.errors.as_json(escape_html=False)),ensure_ascii=False)
            return JsonResponse(ret)

        if not wf_id or not process_step_id:
            ret["result"] = 1
            ret["msg"] = "未从前端接收到工单id 或 流程step id 信息,请刷新重试..." 
            return JsonResponse(ret)
        else:
            process_step_id = int(process_step_id)

        try:
            wf_obj = WorkFormModel.objects.get(id__exact=wf_id)
        except WorkFormModel.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "WorkFormModel 模型不存在 id: %s 的对象,请刷新重试..." %(wf_id)
            wslog_error().error("WorkFormModel 模型不存在 id: %s 的对象" %(wf_id))
            return JsonResponse(ret)

        if int(process_step_id) != wf_obj.process_step_id:
            ret["result"] = 1
            ret["msg"] = "审批失败，因为 WorkFormModel 模型对象 id: %s 流程进度已发生了变化,请刷新..." %(wf_id)
            wslog_error().error("用户 %s 审批失败,WorkFormModel模型对象id: %s 流程进度已不是提交时的进度: process_step_id 为 %s" %(request.user.username,wf_id,process_step_id))
            return JsonResponse(ret)

        if request.user not in wf_obj.approver_can.all():
            ret["result"] = 1
            ret["msg"] = "审批失败，你没有权限审核 WorkFormModel 模型对象 id: %s 流程进度: %s 的工单" %(wf_id,process_step_id)    
            wslog_error().error("用户 %s 审批失败,你没有权限审核 WorkFormModel 模型对象 id: %s 流程进度: %s 的工单" %(request.user.username,wf_id,process_step_id)) 
            return JsonResponse(ret)

        try:
            af_obj = ApprovalFormModel.objects.get(workform_id__exact=wf_id,process_id=process_step_id)
            af_obj.approver = request.user
            af_obj.result = workform_approval_form.cleaned_data.get("result")
            af_obj.approve_note = workform_approval_form.cleaned_data.get("approve_note")
            af_obj.approval_time = datetime.now().strftime("%Y-%m-%d %X")
            af_obj.save()   
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "审批失败，更新 ApprovalFormModel 模型对象 workform_id: %s 流程进度: %s 的工单 审批信息失败,请联系运维同事" %(wf_id,process_step_id)
            wslog_error().error("用户 %s 审批失败,更新 ApprovalFormModel 模型对象 workform_id: %s 流程进度: %s 的工单 审批信息失败,错误信息: %s" %(request.user.username,wf_id,process_step_id,e.args))
            return JsonResponse(ret)
        
        '''插询并确定流程下一个 step_id'''
        wf_process_list = list(wf_obj.approvalformmodel_set.filter(id__gt=af_obj.id).values("id","process_id").order_by("id"))

        if not wf_process_list:
            ret["result"] = 1
            ret["msg"] = "WorkFormModel 模型对象 id: %s 的工单已经流程审批结束,不能再次审批" %(wf_id)
            wslog_error().error("用户 %s 审批失败,WorkFormModel 模型对象 id: %s 的工单已经流程审批结束,不能再次审批" %(request.user.username,wf_id))
            return JsonResponse(ret)

        process_next_id = wf_process_list[0]["process_id"]

        try:
            p_obj = ProcessModel.objects.get(id__exact=process_next_id)
        except ProcessModel.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "ProcessModel 模型中不存在 id: %s 的 step,请联系运维检查..." %(process_next_id)
            return Jsonresponse(ret)
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "ProcessModel 模型查询 id: %s 的对象失败,请查看日志" %(process_next_id)
            wslog_error().error("ProcessModel 模型查询 id: %s 的对象失败,错误信息: %s" %(process_next_id.e.args))
            return Jsonresponse(ret)
        else:
            next_step_id = p_obj.step_id

        ''' 更新工单的状态 '''
        if next_step_id == 60:
            wf_obj.status = "2"
            wf_obj.process_step_id = process_next_id
            wf_obj.approver_can.clear()
        elif  af_obj.result == "2" or af_obj.result == "3":
            wf_obj.status = "3"
            wf_obj.approver_can.set([request.user])
        elif af_obj.result == "1":
            wf_obj.status = "2"
            wf_obj.approver_can.clear()
        else:
            wf_obj.status = "1"
            wf_obj.process_step_id = process_next_id
            wf_obj.approver_can.set(ApprovalFormModel.objects.get(workform_id__exact=wf_id,process_id=process_next_id).approver_can.all())

        try:
            wf_obj.save()
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "审批失败，更新 WorkFormModel 模型对象 id: %s 的工单为最新的流程进度: %s 出现异常,请联系运维同事" %(wf_id,process_next_id)
            wslog_error().error("用户 %s 审批失败,更新 WorkFormModel 模型对象 id: %s 的工单为最新的流程进度: %s 出现异常,错误信息: %s" %(request.user.username,wf_id,process_next_id,e.args))
        else:
            ret["msg"] = "更新 WorkFormModel 模型对象 id: %s 的工单为最新的流程进度: %s 成功" %(wf_id,process_next_id)
            wslog_error().error("用户 %s 更新 WorkFormModel 模型对象 id: %s 的工单为最新的流程进度: %s 成功" %(request.user.username,wf_id,process_next_id)) 

        return JsonResponse(ret)

''' 工单信息查询 '''
class WorkFormInfoView(LoginRequiredMixin,View):

    def get(self,request):

        ret = {"result":0}
        wf_id = request.GET.get("id")

        try:
            wf_obj = WorkFormModel.objects.get(id__exact=wf_id)
        except WorkFormModel.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "WorkFormModel 模型不存在 id: %s 的对象,请刷新重试..." %(wf_id)
            wslog_error().error("WorkFormModel 模型不存在 id: %s 的对象" %(wf_id))
            return JsonResponse(ret)

        try:
            wf_info = WorkFormModel.objects.filter(id__exact=wf_id).values()[0]
            wf_info["level"] = wf_obj.get_level_display()
            wf_info["status"] = wf_obj.get_status_display()
            wf_info["type_id"] = wf_obj.type.cn_name
            wf_info["applicant"] = wf_obj.applicant.userextend.cn_name
            if wf_info.get("create_time"):
                wf_info["create_time"] = utc_to_local(wf_obj.create_time).strftime("%Y-%m-%d %X")
            if wf_info.get("complete_time"):
                wf_info["complete_time"] = utc_to_local(wf_obj.complete_time).strftime("%Y-%m-%d %X")
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "WorkFormModel 模型 id: %s 的对象转 dict 失败,请查看日志..." %(wf_id)
            wslog_error().error("WorkFormModel 模型 id: %s 的对象转 dict 失败,错误信息: %s" %(wf_id,e.args))
        else:
            wslog_info().info("WorkFormModel 模型 id: %s 的对象转 dict 成功,查询该对象的详情成功" %(wf_id))
            ret["wf_info"] = wf_info

        return JsonResponse(ret)


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

