from resources.models import ServerAliyunModel
from django.http import JsonResponse
from django.views.generic import View


class GetServerEnvView(View):
    def get(self,request):
        server_env_choices = list(ServerAliyunModel.ENV_CHOICES)
        return JsonResponse(server_env_choices,safe=False)
