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
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

# Create your views here.

class LoginView(TemplateView):
    template_name = "public/login.html"

    def get_context_data(self,**kwargs):
        context = super(LoginView,self).get_context_data(**kwargs)
        hashkey = CaptchaStore.generate_key()
        context["hashkey"]  = hashkey
        context["image_url"] = captcha_image_url(hashkey)
        return context

    def post(self,request,*args,**kwargs):
        res = {'status':0,'msg':''}

        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        captcha_hashkey = request.POST.get('captcha_0',None)
        captcha_response = request.POST.get('captcha_1',None)

        if not captcha_response:
            res["status"] = 1
            res["msg"] = "请输入验证码"
            return JsonResponse(res)

        try:
            captcha_obj = CaptchaStore.objects.get(response__exact=captcha_response,hashkey__exact=captcha_hashkey)
        except CaptchaStore.DoesNotExist:
            res["status"] = 1
            res["msg"] = "输入的验证码有误，请重新输入或者刷新验证码"
            return JsonResponse(res)

        user = authenticate(username=username,password=password)

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
