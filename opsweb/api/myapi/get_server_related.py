from resources.models import ServerModel,CmdbModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import View


class GetServerEnvView(LoginRequiredMixin,View):
    def get(self,request):
        server_env_choices = list(ServerModel.ENV_CHOICES)
        return JsonResponse(server_env_choices,safe=False)

class GetServerIPView(LoginRequiredMixin,View):

    def post(self,request):
        env = request.POST.get("env")
        cmdb_id = request.POST.get("cmdb_id")
        if cmdb_id:
            ip_list = list(CmdbModel.objects.get(id__exact=int(cmdb_id)).ips.values("id","private_ip"))
        else:
            if not env:
                ip_list = [ {"id":i["id"],"private_ip":i['private_ip']} for i in ServerModel.objects.filter(status__exact="Running").values("id","private_ip")]
            else:
                ip_list = [{"id":i["id"],"private_ip":i['private_ip']} for i in ServerModel.objects.filter(env__exact=env,status__exact="Running").values("id","private_ip")]

        return JsonResponse(ip_list,safe=False)
