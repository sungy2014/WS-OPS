from django.views.generic import ListView,View,TemplateView
from django.contrib.auth.models import Group,User,Permission
from django.http import HttpResponse,JsonResponse,Http404
from django.db.utils import IntegrityError
from django.core.paginator import Paginator


class GroupListView(ListView):
    template_name = "group/group_list.html"
    model = Group
    paginate_by = 10
    ordering = "id"

class GroupAddView(View):
    def post(self,request):
        name = request.POST.get('name',None)
        ret = {'result':0,'msg':None}
        if not name:
            ret['result'] = 1
            ret['msg'] = "组名不能为空"
            return JsonResponse(ret)
        try:
            group = Group(name=name)
            group.save()
            ret['msg'] = "组添加成功"
        except IntegrityError:
            ret['result'] = 1
            ret['msg'] = "该用户组已经存在"
        except Exception as e:
            ret['result'] = 1
            ret['msg'] = e.args
        return JsonResponse(ret)

class GroupDeleteView(View):
    def post(self,request):
        id = request.POST.get('id',0)
        ret = {'result':0,'msg':'Null'}
        try:
            g = Group.objects.filter(id=id)
            g.delete()
            ret['msg'] = "用户组删除成功"
        except Group.DoesNotExist:
            ret['result'] = 1
            ret['msg'] = "该用户组不存在"

        return JsonResponse(ret)
            
class GroupUserListView(TemplateView):
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

class GroupUserDeleteView(View):
    def post(self,request):
        uid = request.POST.get('uid',0)
        gid = request.POST.get('gid',0)
        ret = {'result':0,'msg':None}
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

class GroupPermissionListView(TemplateView):
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
        gid = request.POST.get("id",0)
        perms_list = request.POST.getlist("group_permissions",None)
        ret = {'result':0,'msg':None}

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

class GroupPermissionDeleteView(View):
    def get(self,request):
        group_id = request.GET.get("gid",0)
        perm_id = request.GET.get("perm_id",0)
        ret = {'result':0,'msg':None}

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
