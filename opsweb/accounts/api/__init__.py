from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View,TemplateView,ListView
from django.http import JsonResponse

class GetGroupInfoView(LoginRequiredMixin,View):
    def get(self,request):
        group_list = list(Group.objects.values("id","name")) 
        return JsonResponse(group_list,safe=False)
