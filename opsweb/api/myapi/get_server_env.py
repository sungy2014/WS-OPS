from resources.models import Server_Aliyun
from django.http import JsonResponse
from django.views.generic import View


class GetServerEnvView(View):
    def get(self,request):
        server_env_choices = list(Server_Aliyun.ENV_CHOICES)
        return JsonResponse(server_env_choices,safe=False)
