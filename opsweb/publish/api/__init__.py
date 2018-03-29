from django.http import JsonResponse
from django.views.generic import TemplateView,ListView,View
from dashboard.utils.wslog import wslog_error,wslog_info
from resources.models import CmdbModel
from publish.models import PublishVersionModel
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


class PublishJenkinsApiView(View):
    def post(self,request):
        ret = {"result":0}
        version = request.POST.get('version')
        module_name = request.POST.get('module_name')
        try:
            PublishVersionModel.objects.get(version__exact=version)
        except PublishVersionModel.DoesNotExist:
            pass
        else:
            ret["result"] = 1
            ret["msg"] = "版本: %s 已经存在" %(version)
            wslog_error().error("jenkis post 打包信息失败,版本记录表中已经存在该版本: %s" %(version))

        try:
            m_obj = CmdbModel.objects.get(name__exact=module_name)
        except CmdbModel.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "modelu_name: %s 不存在,因此jenkins打包的版本不能写库" %(module_name)
            wslog_error().error(ret["msg"])
        else:
            version_info = request.POST.copy()
            version_info.pop("module_name")

        try:
            pv_obj = PublishVersionModel(**version_info.dict())
            pv_obj.module_name = m_obj
            pv_obj.save()
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "jenkins打包的版本: %s 不能写库,请查看日志" %(version)
            wslog_error().error("jenkins打包的版本: %s 不能写库,错误日志: %s" %(version,e.args))
        else:
            ret["msg"] = "jenkins打包的版本: %s post 成功" %(version)
            wslog_info().info(ret["msg"])
        return JsonResponse(ret)

class GetPublishVersionView(LoginRequiredMixin,View):
    def post(self,request):
        ret = {"result":0}
        m_id = request.POST.get("cmdb_id")
        type = request.POST.get("type")

        if not m_id or not type:
            ret["result"] = 1
            ret["msg"] = "未收到前端传过来的值"
            return JsonResponse(ret)

        try:
           m_obj = CmdbModel.objects.get(id__exact=m_id) 
        except CmdbModel.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "modelu_name: %s 不存在,因此不能查询其相应的打包版本" %(module_name)
            wslog_error().error(ret["msg"])
            return JsonResponse(ret)
        
        if type == 'publish':
            ret["version_list"] = list(m_obj.publishversionmodel_set.filter(Q(status__exact="packed")|Q(status__exact="running")).order_by("-id")[:5].values("id","version","pack_user","status"))
        else:
            ret["version_list"] = list(m_obj.publishversionmodel_set.filter(Q(status__exact="running")|Q(status__exact="run_pre")).order_by("-id")[:5].values("id","version","pack_user","status")) 

        return JsonResponse(ret)

