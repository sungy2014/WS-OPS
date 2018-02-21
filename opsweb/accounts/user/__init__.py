from django.views.generic import ListView,View,TemplateView
from django.contrib.auth.models import User,Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse,HttpResponse
from accounts.forms import UserAddForm,UserInfoChangePwdForm,UserInfoChangeForm,UserExtendAddForm
from accounts.permission.permission_required_mixin import PermissionRequiredMixin
from accounts.models import UserExtend
import json
from django.db.models import Q
from dashboard.utils.wslog import wslog_error,wslog_info
from django.contrib.auth import update_session_auth_hash

''' 用户列表 '''
class UserListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = "auth.view_user"
    permission__redirect_url = "index"

    template_name = "user/users_list.html"
    model = User
    paginate_by = 10
    # page_total 是指前端要显示的总页数
    page_total = 11
    ordering = 'id'

    def get_context_data(self,**kwargs):
        context = super(UserListView,self).get_context_data(**kwargs)
        context['page_range'] = self.get_page_range(context['page_obj'])
        context["role"] = dict(UserExtend.ROLE_CHOICES)
        # request.GET 是获取QueryDict对象,也即是前端传过来的所有参数,由于QueryDict对象是只读的,所有要使用copy方法,赋值一份出来,才能进行修改
        search_data = self.request.GET.copy()
        try:
            search_data.pop('page')
        except:
            pass

        if search_data:
            context['search_uri'] = '&' + search_data.urlencode()
        else:
            context['search_uri'] = '' 
        # context.update(字典A) 是合并字典 context 和 A
        context.update(search_data.dict())
        return context

    # 过滤模型中的数据
    def get_queryset(self):
        queryset = super(UserListView,self).get_queryset()
        queryset = queryset.filter(is_superuser=False)
        queryset = queryset.exclude(username__exact=self.request.user)

        search_name = self.request.GET.get('search',None)
        if search_name:
            queryset = queryset.filter(Q(username__icontains=search_name)|Q(userextend__phone__icontains=search_name))
        return queryset
    
    # 获取要展示的页数范围,这里是固定显示多少页
    def get_page_range(self,page_obj):
        page_now = page_obj.number
        if page_obj.paginator.num_pages > self.page_total:
            page_start = page_now - self.page_total//2
            page_end = page_now + self.page_total//2 + 1

            if page_start <= 0:
                page_start = 1
                page_end = page_start + self.page_total
            if page_end > page_obj.paginator.num_pages:
                page_end = page_obj.paginator.num_pages + 1
                page_start = page_end - self.page_total
        else:
            page_start = 1
            page_end = page_obj.paginator.num_pages + 1

        page_range = range(page_start,page_end)
        return page_range

''' 修改用户状态 '''
class UserModifyStatusView(LoginRequiredMixin,View):
    permission_required = "auth.change_user"

    def post(self,request,*args,**kwargs):
        ret={'result':0}

        ## ajax 请求的权限验证
        if not request.user.has_perm(self.permission_required):
            ret["result"] = 1
            ret["msg"] = "Sorry,你没有权限,请联系运维!"
            return JsonResponse(ret) 

        id = request.POST.get("id",0)
        try:
            user = User.objects.get(id=id)
            user.is_active = True if user.is_active == False else False
            user.save()
            ret["msg"]="修改成功"
        except User.DoesNotExist:
            ret["result"]=1
            ret["msg"]="用户不存在"
        return JsonResponse(ret)

''' 修改用户所属组 '''
class UserModifyGroupView(LoginRequiredMixin,View):
    permission_required = "auth.change_user"

    def get(self,request):
        ret = {'result':0,'msg':None}

        ## ajax 请求的权限验证
        if not request.user.has_perm(self.permission_required):
            ret["result"] = 1
            ret["msg"] = "Sorry,你没有权限,请联系运维!"
            return JsonResponse(ret)

        uid = request.GET.get('id',0)

        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            ret['result'] = 1
            ret['msg'] = "该用户不存在"
            return JsonResponse(ret)
        user_group = list(user_obj.groups.values('id')) 
        group_list = list(Group.objects.values('id','name'))
        ret['user_group'] = user_group
        ret['group_list'] = group_list
        return JsonResponse(ret)

    def post(self,request):
        ret = {'result':0,'msg':None}

        ## ajax 请求的权限验证
        if not request.user.has_perm(self.permission_required):
            ret["result"] = 1
            ret["msg"] = "Sorry,你没有权限,请联系运维!"
            return JsonResponse(ret)

        uid = request.POST.get('id',None)
        gid_list = request.POST.getlist('group_name',None)

        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            ret['result'] = 1
            ret['msg'] = "该用户不存在"
            return JsonResponse(ret)

        if not gid_list:
            ret['result'] = 1
            ret['msg'] = "请选择至少一个组名"
            return JsonResponse(ret)

        try:
            group_obj_list = [Group.objects.get(id=gid) for gid in gid_list]
        except Group.DoesNotExist:
            ret['result'] = 1
            ret['msg'] = "用户组不存在"
            return JsonResponse(ret)
        
        try:
            user_obj.groups.set(group_obj_list)
        except Exception as e:
            ret['result'] = 1
            ret['msg'] = "用户: %s 修改组信息失败,错误信息: %s" %(user_obj.username,e.args)
        else:
            ret['msg'] = "用户: %s 组修改成功" %(user_obj.username)

        return JsonResponse(ret)

''' ldap 用户第一次登陆后需要完善个人资料 '''        
class UserExtendAddView(LoginRequiredMixin,TemplateView):
    template_name = "user/userextend_add.html"
    
    def get_context_data(self,**kwargs):
        context = super(UserExtendAddView,self).get_context_data(**kwargs)
        u_obj = self.request.user 
        context["id"] = u_obj.id
        context["username"] = u_obj.username
        context["role"] = dict(UserExtend.ROLE_CHOICES)
        return context

    def post(self,request):
        ret={"result":0}

        u_obj = request.user

        user_extend_add_form = UserExtendAddForm(request.POST)

        if not user_extend_add_form.is_valid():
            ret["result"] = 1
            error_msg = json.loads(user_extend_add_form.errors.as_json(escape_html=False))
            ret["msg"] = '\n'.join([ i["message"] for v in error_msg.values() for i in v ])
            return JsonResponse(ret)

        try:
            u_obj.set_password(user_extend_add_form.cleaned_data.get("password"))
            u_obj.save(update_fields=["password"])
            u_obj.save()
            update_session_auth_hash(request, u_obj)
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "User 模型对象: %s 修改密码失败,请查看日志" %(uid)
            wslog_error().error("User 模型对象: %s 修改密码失败，错误信息: %s" %(uid,e.args))
            return JsonResponse(ret)
        else:
            del user_extend_add_form.cleaned_data["password"]

        try:
            ue_obj = UserExtend(**user_extend_add_form.cleaned_data)
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = "UserExtend 模型对象: %s 添加失败,请查看日志" %(user_extend_add_form.cleaned_data.get("cn_name"))
            wslog_error().error("UserExtend 模型对象: %s 添加失败，错误信息: %s" %(user_extend_add_form.cleaned_data.get("cn_name"),e.args))
        else:
            ue_obj.user = u_obj
            ue_obj.save()
            ret["msg"] = "UserExtend 模型对象: %s 添加成功" %(user_extend_add_form.cleaned_data.get("cn_name"))
         
        return JsonResponse(ret)

''' 添加/注册 用户 '''
class UserAddView(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    permission_required = "auth.add_user"
    permission__redirect_url = "users_list"

    template_name = "user/users_add.html"

    def get_context_data(self):
        context = super(UserAddView,self).get_context_data()
        context["role"] = dict(UserExtend.ROLE_CHOICES)
        return context

    def post(self,request):
        ret = {"result":0,"msg":None}

        ## ajax 请求的权限验证
        if not request.user.has_perm(self.permission_required):
            ret["result"] = 1
            ret["msg"] = "Sorry,你没有权限,请联系运维!"
            return JsonResponse(ret)

        user_form = UserAddForm(request.POST)

        if not user_form.is_valid():
            ret["result"] = 1
            error_msg = json.loads(user_form.errors.as_json(escape_html=False)) 
            ret["msg"] = '\n'.join([ i["message"] for v in error_msg.values() for i in v ])
            return JsonResponse(ret)
    
        try:
            user_info = user_form.cleaned_data
            ue_obj = UserExtend()
            user = User.objects.create_user(user_info.get('username'),user_info.get("email"),user_info.get("password"))
            ue_obj.user = user
            user.userextend.cn_name = user_info.get('cn_name')
            user.userextend.phone = user_info.get('phone')
            user.userextend.role = user_info.get('role')
            user.userextend.save()
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = e.args
        else:
            ret["msg"] = "新用户 %s 注册成功" %(user_info.get('username'))

        return JsonResponse(ret)


''' 删除用户 '''
class UserDeleteView(LoginRequiredMixin,View):
    permission_required = "auth.delete_user"

    def get(self,request):
        ret = {"result":0,"msg":None}
        
        ## ajax 请求的权限验证
        if not request.user.has_perm(self.permission_required):
            ret["result"] = 1
            ret["msg"] = "Sorry,你没有权限,请联系运维!"
            return JsonResponse(ret)

        uid = request.GET.get("uid",0)

        try:
            user_obj = User.objects.get(id__exact=uid)
        except User.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "该用户不存在"
            return JsonResponse(ret)

        try:
            user_obj.delete()
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = e.args
        else:
            ret["msg"] = "用户 %s 删除成功" %(user_obj.username)

        return JsonResponse(ret)


''' 用户个人中心 '''
class UserInfoView(LoginRequiredMixin,TemplateView):
    template_name = "user/user_info.html"
    
    def get_context_data(self,**kwargs):
        context = super(UserInfoView,self).get_context_data(**kwargs)
        context['user_info'] = self.request.user
        context["role"] = dict(UserExtend.ROLE_CHOICES)
        return context


''' 修改用户信息：用户个人中心 和 用户列表中的"更新用户信息"共用此逻辑 '''
class UserInfoChangeView(LoginRequiredMixin,View):
    permission_required = "auth.change_user"

    def get(self,request):
        ret = {"result":0,"msg":None}

        ## ajax 请求的权限验证
        if not request.user.has_perm(self.permission_required):
            ret["result"] = 1
            ret["msg"] = "Sorry,你没有权限,请联系运维!"
            return JsonResponse(ret)

        user_info = {}
        uid = request.GET.get("id",0)
        try:
            user_obj = User.objects.get(id__exact=uid)
        except User.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "该用户ID %s 不存在" %(uid)
        else:
            user_info['username'] = user_obj.username
            user_info['email'] = user_obj.email
            user_info['cn_name'] = user_obj.userextend.cn_name
            user_info['phone'] = user_obj.userextend.phone
            user_info['role'] = user_obj.userextend.role
            ret["user_obj"] = user_info

        return JsonResponse(ret)

    def post(self,request):
        ret = {"result":0,"msg":None}

        ## ajax 请求的权限验证
        if not request.user.has_perm(self.permission_required) and request.META.get('HTTP_REFERER','/').find("/accounts/users/list") != -1:
            ret["result"] = 1
            ret["msg"] = "Sorry,你没有权限,请联系运维!"
            return JsonResponse(ret)

        uid = request.POST.get("id",0)
        user_change_form = UserInfoChangeForm(request.POST)
        if not user_change_form.is_valid():
            ret["result"] = 1
            error_msg = json.loads(user_change_form.errors.as_json(escape_html=False))
            ret["msg"] = '\n'.join([ i["message"] for v in error_msg.values() for i in v ])
            return JsonResponse(ret)
        try:
            user_obj = User.objects.get(id__exact=uid)
        except User.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "该用户ID %s 不存在,请刷新重试......" %(uid)
            return JsonResponse(ret)
        try:
            user_obj.email = user_change_form.cleaned_data.get("email")
            user_obj.userextend.cn_name = user_change_form.cleaned_data.get("cn_name")
            user_obj.userextend.phone = user_change_form.cleaned_data.get("phone")
            user_obj.userextend.role = user_change_form.cleaned_data.get("role")
            user_obj.save(update_fields=["email"])
            user_obj.userextend.save(update_fields=["cn_name","phone","role","last_change_time"])
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = e.args
        else:
            ret["msg"] = "用户 %s 更新信息成功" %(User.objects.get(id__exact=uid).username)

        return JsonResponse(ret)


''' 修改用户密码：用户个人中心 和 用户列表中的"更新密码"共用此逻辑 '''
class UserInfoChangePwdView(LoginRequiredMixin,View):
    permission_required = "auth.change_user"

    def post(self,request):
        ret = {"result":0,"msg":None}

        ## ajax 请求的权限验证
        if not request.user.has_perm(self.permission_required) and request.META.get('HTTP_REFERER','/').find("/accounts/users/list") != -1:
            ret["result"] = 1
            ret["msg"] = "Sorry,你没有权限,请联系运维!"
            return JsonResponse(ret)

        uid = request.POST.get("id",0)
        user_changepwd_form = UserInfoChangePwdForm(request.POST)
        if not user_changepwd_form.is_valid():
            ret["result"] = 1
            error_msg = json.loads(user_changepwd_form.errors.as_json(escape_html=False)) 
            ret["msg"] = '\n'.join([ i["message"] for v in error_msg.values() for i in v ])
            return JsonResponse(ret)
        try:
            user_obj = User.objects.get(id__exact=uid)
        except User.DoesNotExist:
            ret["result"] = 1
            ret["msg"] = "该用户ID %s 不存在,请刷新重试......" %(uid)
            return JsonResponse(ret)
            
        try:
            user_obj.set_password(user_changepwd_form.cleaned_data.get('password'))
            user_obj.save(update_fields=['password'])
            user_obj.userextend.save(update_fields=["last_change_time"])
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = e.args
        else:
            ret["msg"] = "用户%s 更新密码成功,需要重新登录......" %(user_obj.username)

        return JsonResponse(ret)
