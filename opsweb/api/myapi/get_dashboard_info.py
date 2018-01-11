from django.views.generic import View
from django.http import JsonResponse
from resources.models import ServerStatisticByDayModel,CmdbStatisticByDayModel,ServerModel,CmdbModel
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.utils.wslog import wslog_error,wslog_info
from datetime import *


class GetServerStatisticView(LoginRequiredMixin,View):
    def get(self,request):

        my_yesterday = (date.today() - timedelta(days=1)).isoformat()
        count = count = ServerModel.objects.count()

        try:
            ssbd_obj = ServerStatisticByDayModel.objects.get(myday__exact=my_yesterday)
        except ServerStatisticByDayModel.DoesNotExist:
            wslog_error().error("模型 ServerStatisticByDayModel 获取对象 %s 失败,不存在这个对象" %(myday))
            count_yesterday = 0
        else:
            count_yesterday = ssbd_obj.count
        return JsonResponse({"count":count,"compared_with_yesterday":str(count-count_yesterday)})

class GetCmdbStatisticView(LoginRequiredMixin,View):
    def get(self,request):

        my_yesterday = (date.today() - timedelta(days=1)).isoformat()
        count = CmdbModel.objects.count()
        try:
            csbd_obj = CmdbStatisticByDayModel.objects.get(myday__exact=my_yesterday)
        except CmdbStatisticByDayModel.DoesNotExist:
            wslog_error().error("模型 CmdbStatisticByDayModel 获取对象 %s 失败,不存在这个对象" %(myday))
            count_yesterday = 0
        else:
            count_yesterday = csbd_obj.count
        return JsonResponse({"count":count,"compared_with_yesterday":str(count-count_yesterday)})
