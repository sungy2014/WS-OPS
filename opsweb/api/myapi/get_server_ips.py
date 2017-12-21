from resources.models import ServerAliyunModel
from django.views.generic import View
from django.http import JsonResponse

class GetServerIPView(View):

    def post(self,request):
        env = request.POST.get("env")
        if not env:
            ip_list = [ {"id":i["id"],"private_ip":i['private_ip']} for i in ServerAliyunModel.objects.filter(status__exact="Running").values("id","private_ip")]
        else:
            ip_list = [{"id":i["id"],"private_ip":i['private_ip']} for i in ServerAliyunModel.objects.filter(env__exact=env,status__exact="Running").values("id","private_ip")]

        return JsonResponse(ip_list,safe=False)
