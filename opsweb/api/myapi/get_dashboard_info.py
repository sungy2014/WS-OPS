from django.views.generic import View
from django.http import JsonResponse
from resources.models import ServerStatisticByDayModel,CmdbStatisticByDayModel
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.utils.wslog import wslog_error,wslog_info
from datetime import *


class GetServerStatisticView(LoginRequiredMixin,View):
    def get(self,request):
        ret = {"result":0,"msg":None}

        myday = date.today().isoformat()
        try:
            ssbd_obj = ServerStatisticByDayModel.objects.get(myday__exact=myday)
        except ServerStatisticByDayModel.DoesNotExist:
            wslog_error().error("模型 ServerStatisticByDayModel 获取对象 %s 失败,不存在这个对象" %(myday))
            return JsonResponse({"count":0,"compared_with_yesterday":0})
        else:
            return JsonResponse({"count":ssbd_obj.count,"compared_with_yesterday":ssbd_obj.compared_with_yesterday})

class GetCmdbStatisticView(LoginRequiredMixin,View):
    def get(self,request):
        ret = {"result":0,"msg":None}

        myday = date.today().isoformat()
        try:
            csbd_obj = CmdbStatisticByDayModel.objects.get(myday__exact=myday)
        except CmdbStatisticByDayModel.DoesNotExist:
            wslog_error().error("模型 CmdbStatisticByDayModel 获取对象 %s 失败,不存在这个对象" %(myday))
            return JsonResponse({"count":0,"compared_with_yesterday":0})
        else:
            return JsonResponse({"count":csbd_obj.count,"compared_with_yesterday":csbd_obj.compared_with_yesterday})
