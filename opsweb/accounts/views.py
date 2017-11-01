from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
#from django.urls import reverse    1.11
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_view(request):
    if request.method == "GET":
        return render(request,"public/login.html")
    else:
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = authenticate(username=username,password=password)
        res = {'status':0,'errmsg':''}
        print ("request_body:",request.body)
        if user:
            if user.is_active:
                login(request,user)
                res['errmsg'] = "登录成功"
                res['next_url'] = request.GET.get('next') if request.GET.get('next',None) else '/'
            else:
                res['status'] = 1
                res['errmsg'] = "用户被锁定"
        else:
            res['status'] = 1
            res['errmsg'] = "用户验证失败"

        return JsonResponse(res)

def logout_view(request):
    logout(request)
    print ("reverse_login:",reverse("user_login"))
    return HttpResponseRedirect(reverse("user_login"))
