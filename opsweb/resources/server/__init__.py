from django.views.generic import View,TemplateView,ListView
from django.http import JsonResponse

class ServerListView(View):
    def get(self,request):
        return JsonResponse({})
