from django.views.generic import ListView,View
from django.contrib.auth.models import User,Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse,HttpResponse

class UserListView(LoginRequiredMixin,ListView):
    template_name = "user/userlist.html"
    model = User
    paginate_by = 10
    # page_total 是指前端要显示的总页数
    page_total = 11
    ordering = 'id'

    def get_context_data(self,**kwargs):
        context = super(UserListView,self).get_context_data(**kwargs)
        context['page_range'] = self.get_page_range(context['page_obj'])
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

        search_name = self.request.GET.get('search',None)
        if search_name:
            queryset = queryset.filter(username__icontains=search_name)
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


class UserModifyStatusView(View):
    def post(self,request,*args,**kwargs):
        id = request.POST.get("id",None)
        ret={'result':0}
        try:
            user = User.objects.get(id=id)
            user.is_active = True if user.is_active == False else False
            user.save()
            ret["msg"]="修改成功"
        except User.DoesNotExist:
            ret["result"]=1
            ret["msg"]="用户不存在"
        return JsonResponse(ret)

class UserModifyGroupView(View):
    def get(self,request):
        uid = request.GET.get('id',None)
        ret = {'result':0,'msg':None}
        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            ret['result'] = 1
            ret['msg'] = "该用户不存在"
            return JsonResponse(ret)
        user_group = list(user.groups.values('id')) 
        group_list = list(Group.objects.values('id','name'))
        ret['user_group'] = user_group
        ret['group_list'] = group_list
        return JsonResponse(ret)

    def post(self,request):
        uid = request.POST.get('id',None)
        gid_list = request.POST.getlist('group_name',None)
        ret = {'result':0,'msg':None}
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            ret['result'] = 1
            ret['msg'] = "该用户不存在"
            return JsonResponse(ret)

        try:
            group_obj_list = [Group.objects.get(id=gid) for gid in gid_list]
        except Group.DoesNotExist:
            ret['result'] = 1
            ret['msg'] = "用户组不存在"
            return JsonResponse(ret)
        user_obj.groups.set(group_obj_list)
        ret['msg'] = "组修改成功"
        return JsonResponse(ret)

