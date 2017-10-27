from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import View,TemplateView,ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class LoginView(TemplateView):
    template_name = "public/login.html"

    def post(self,request,*args,**kwargs):
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = authenticate(username=username,password=password)
        res = {'status':0,'msg':''}
        print ("request_body:",request.body)
        if user:
            if user.is_active:
                login(request,user)
                res['msg'] = "登录成功"
                res['next_url'] = request.GET.get('next') if request.GET.get('next',None) else '/'
            else:
                res['status'] = 1
                res['msg'] = "用户被锁定"
        else:
            res['status'] = 1
            res['msg'] = "用户验证失败"

        return JsonResponse(res)

class LogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("user_login"))
