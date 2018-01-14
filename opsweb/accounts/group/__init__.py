from django.views.generic import ListView,View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group,User,Permission
from django.http import HttpResponse,JsonResponse,Http404
from django.db.utils import IntegrityError
from accounts.permission.permission_required_mixin import PermissionRequiredMixin
from django.core.paginator import Paginator
from accounts.forms import GroupAddForm
import json


class GroupListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = "auth.view_group"
    permission_redirect_url = "index"

    template_name = "group/group_list.html"
    model = Group
    paginate_by = 10
    ordering = "id"

class GroupAddView(LoginRequiredMixin,View):
    permission_required = "auth.add_group"

    def post(self,request):
        ret = {'result':0,'msg':None}

        ## ajax 请求的权限验证
        if not request.user.has_perm(self.permission_required):
            ret["result"] = 1
            ret["msg"] = "Sorry,你没有'添加组'的权限,请联系运维!"
            return JsonResponse(ret) 

        group_form = GroupAddForm(request.POST)
        if not group_form.is_valid():
            ret['result'] = 1
            ret['msg'] = json.dumps(json.loads(group_form.errors.as_json(escape_html=False)),ensure_ascii=False)
            return JsonResponse(ret)
        try:
            group = Group(**group_form.cleaned_data)
            group.save()
            ret['msg'] = "组 %s 添加成功" %(group_form.cleaned_data.get("name"))
        except Exception as e:
            ret['result'] = 1
            ret['msg'] = e.args
        return JsonResponse(ret)

class GroupDeleteView(LoginRequiredMixin,View):
    permission_required = "auth.delete_group"

    def post(self,request):
        id = request.POST.get('id',0)
        ret = {'result':0,'msg':'Null'}

        ## ajax 请求的权限验证
        if not request.user.has_perm(self.permission_required):
            ret["result"] = 1
            ret["msg"] = "Sorry,你没有'删除组'的权限,请联系运维!"
            return JsonResponse(ret) 

        try:
            g = Group.objects.filter(id=id)
            g.delete()
            ret['msg'] = "用户组删除成功"
        except Group.DoesNotExist:
            ret['result'] = 1
            ret['msg'] = "该用户组不存在"

        return JsonResponse(ret)
            
class GroupUserListView(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    permission_required = "auth.view_group_user"
    permission_redirect_url = "group_list"

    template_name = "group/group_user_list.html"

    def get_context_data(self,**kwargs):
        context = super(GroupUserListView,self).get_context_data(**kwargs)
        self.page_num = int(self.request.GET.get("page",1))
        self.page_by = 10
        gid = self.request.GET.get('gid',0)

        try:
            group_obj = Group.objects.get(id=gid)
        except Group.DoesNotExist:
            raise Http404("组不存在")
        else:
            context['page_obj'] = Paginator(group_obj.user_set.all(),self.page_by).page(self.page_num)
            context['object_list'] = context['page_obj'].object_list
            context['group_obj'] = group_obj

        return context

class GroupUserDeleteView(LoginRequiredMixin,View):
    permission_required = "auth.delete_group_user"

    def post(self,request):
        ret = {'result':0,'msg':None}

        ## ajax 请求的权限验证
        if not request.user.has_perm(self.permission_required):
            ret["result"] = 1
            ret["msg"] = "Sorry,你没有'删除组下面用户'的权限,请联系运维!"
            return JsonResponse(ret)

        uid = request.POST.get('uid',0)
        gid = request.POST.get('gid',0)

        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            ret['result'] = 1
            ret['msg'] = "用户不存在"
            return JsonResponse(ret)
        try:
            group_obj = Group.objects.get(id=gid)
        except Group.DoesNotExist:
            ret['result'] = 1
            ret['msg'] = "组不存在"
            return JsonResponse(ret)
        group_obj.user_set.remove(user_obj)
        ret['msg'] = "组%s内删除用户%s成功" %(group_obj.name,user_obj.username)
        return JsonResponse(ret)

class GroupPermissionListView(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    permission_required = "auth.view_group_permission"
    permission_redirect_url = "group_list"

    template_name = "group/group_permission_list.html"

    def get_context_data(self,**kwargs):
        context = super(GroupPermissionListView,self).get_context_data(**kwargs)
        self.page_num = int(self.request.GET.get("page",1))
        self.page_by = 10
        gid = self.request.GET.get('gid',0)

        try:
            g_obj = Group.objects.get(id__exact=gid)
        except Group.DoesNotExist:
            raise Http404("该组 ID 不存在")
        else:
            context['page_obj'] = Paginator(g_obj.permissions.all(),self.page_by).page(self.page_num)
            context['object_list'] = context['page_obj'].object_list 
            context['g_exclude_perms_list'] = Permission.objects.exclude(id__in=g_obj.permissions.values_list("id"))
            context['group_obj'] = g_obj
        return context

    def post(self,request):
        ret = {'result':0,'msg':None}

        ## ajax 请求的权限验证
        if not request.user.has_perm(self.permission_required):
            ret["result"] = 1
            ret["msg"] = "Sorry,你没有'添加组权限'的权限,请联系运维!"
            return JsonResponse(ret)

        gid = request.POST.get("id",0)
        perms_list = request.POST.getlist("group_permissions",None)

        try:
            group_obj = Group.objects.get(id=gid)
        except Group.DoesNotExist:
            ret['result'] = 1
            ret['msg'] = "组 ID:%s 不存在" %(gid)
            return JsonResponse(ret)
        if not perms_list:
            ret['result'] = 1
            ret['msg'] = "未选择任何权限,请选择......"
            return JsonResponse(ret)

        perms_obj_list = list(Permission.objects.filter(id__in=perms_list))

        try:
            for perm_obj in perms_obj_list:
                group_obj.permissions.add(perm_obj)
            ret['msg'] = "权限添加成功"
        except Exception as e:
            ret['result'] = 1
            ret['msg'] = e.args
        return JsonResponse(ret)

class GroupPermissionDeleteView(LoginRequiredMixin,View):
    permission_required = "auth.delete_group_permission"

    def get(self,request):
        ret = {'result':0,'msg':None}

        ## ajax 请求的权限验证
        if not request.user.has_perm(self.permission_required):
            ret["result"] = 1
            ret["msg"] = "Sorry,你没有'删除组权限'的权限,请联系运维!"
            return JsonResponse(ret)

        group_id = request.GET.get("gid",0)
        perm_id = request.GET.get("perm_id",0)

        try:
            group_obj = Group.objects.get(id__exact=group_id)
        except GroupDoesNotExist:
            ret['result'] = 1
            ret['msg'] = "组 ID:%s 不存在" %(group_id)
            return JsonResponse(ret)

        try:
            perm_obj = Permission.objects.get(id__exact=perm_id)
        except GroupDoesNotExist:
            ret['result'] = 1
            ret['msg'] = "权限 ID:%s 不存在" %(perm_id)
            return JsonResponse(ret)

        try:
            group_obj.permissions.remove(perm_obj)
            ret['msg'] = "权限删除成功"
        except Exception as e:
            ret['result'] = 1
            ret['msg'] = e.args

        return JsonResponse(ret)
