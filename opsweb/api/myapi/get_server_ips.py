from resources.models import ServerAliyunModel
from django.views.generic import View
from django.http import JsonResponse

class GetServerIPView(View):

    def get(self,request):
        ip_list = [ {"id":i["id"],"private_ip":i['private_ip']} for i in ServerAliyunModel.objects.values("id","private_ip")]
        return JsonResponse(ip_list,safe=False)
