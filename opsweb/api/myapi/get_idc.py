from resources.models import IDC
from django.http import JsonResponse
from django.views.generic import View


class GetIdcListView(View):

    def get(self,request):
        idc_list = list(IDC.objects.values("id","cn_name"))
        return JsonResponse({"idc_list":idc_list})
    
