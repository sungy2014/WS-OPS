from django import forms
from django.contrib.auth.models import Group,ContentType


class GroupAddForm(forms.Form):
    name = forms.CharField(required=True,error_messages={"invalid":"组名不能为空"})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        try:
            Group.objects.get(name__exact=name)
        except Group.DoesNotExist:
            return name 
        except Exception as e:
            raise forms.ValidationError(e.args)
        else:
            raise forms.ValidationError("用户组已存在,请尝试新的组名")


class PermissionAddForm(forms.Form):
    content_type = forms.IntegerField(required=True)
    codename = forms.CharField(required=True,error_messages={"invalid":"codename 不能为空"})
    name = forms.CharField(required=True,error_messages={"invalid":"name 不能为空"})

    def clean_content_type(self):
        content_type_id = self.cleaned_data.get("content_type")
        try:
            content_type_obj = ContentType.objects.get(id__exact=content_type_id)
        except ContentType.DoesNotExist:
            raise forms.ValidationError("App-Model 不存在")
        else:
            return content_type_obj
    
    def clean_codename(self):
        codename = self.cleaned_data.get("codename")
        content_type_obj = self.cleaned_data.get("content_type")
        permissons_list = ['add','delete','change','view']
        if codename.find("_") == -1:
            raise forms.ValidationError("codename 需要用下划线_连接权限和model")
        if codename.find(" ") >= 0:
            raise forms.ValidationError("codename 不能有空格")
        codename_list = codename.split("_",1)
        if codename_list[0] not in permissons_list:
            raise forms.ValidationError("codename的权限操作必须是'增:add 删:delete 改:change 查:view'")
        if codename_list[1] != content_type_obj.model:
            raise forms.ValidationError("codename 必须以模型名结尾")
        if content_type_obj.permission_set.filter(codename__exact=codename): 
            raise forms.ValidationError("codename 在同一content_type 中必须唯一")
        return codename
        
