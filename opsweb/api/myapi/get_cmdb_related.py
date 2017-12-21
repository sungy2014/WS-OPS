from resources.models import CmdbModel
from django.http import JsonResponse
from django.views.generic import View
import json

class GetCmdbEnvView(View):
    def get(self,request):
        env_list = list(CmdbModel.ENV_CHOICES)
        return JsonResponse(env_list,safe=False)

class GetCmdbTypeView(View):
    def get(self,request):
        type_list = list(CmdbModel.TYPE_CHOICES)
        return JsonResponse(type_list,safe=False)

class GetCmdbWayView(View):
    def get(self,request):
        way_list = list(CmdbModel.WAY_CHOICES)
        return JsonResponse(way_list,safe=False)

