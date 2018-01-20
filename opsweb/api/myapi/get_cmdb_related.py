from resources.models import CmdbModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import View
import json

class GetCmdbEnvView(LoginRequiredMixin,View):
    def get(self,request):
        env_list = list(CmdbModel.ENV_CHOICES)
        return JsonResponse(env_list,safe=False)

class GetCmdbTypeView(LoginRequiredMixin,View):
    def get(self,request):
        type_list = list(CmdbModel.TYPE_CHOICES)
        return JsonResponse(type_list,safe=False)

class GetCmdbWayView(LoginRequiredMixin,View):
    def get(self,request):
        way_list = list(CmdbModel.WAY_CHOICES)
        return JsonResponse(way_list,safe=False)

class GetCmdbNameView(LoginRequiredMixin,View):
    def get(self,request):
        cmdb_name_list = list(CmdbModel.objects.filter(env__exact="online").values("id","name"))
        return JsonResponse(cmdb_name_list,safe=False)
