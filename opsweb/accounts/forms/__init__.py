from django import forms
from django.contrib.auth.models import Group,ContentType,User


class GroupAddForm(forms.Form):
    name = forms.CharField(required=True,error_messages={"required":"组名不能为空"})

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
    codename = forms.CharField(required=True,error_messages={"required":"codename 不能为空"})
    name = forms.CharField(required=True,error_messages={"required":"name 不能为空"})

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
#        if codename_list[1] != content_type_obj.model:
#            raise forms.ValidationError("codename 必须以模型名结尾")
        if content_type_obj.permission_set.filter(codename__exact=codename): 
            raise forms.ValidationError("codename 在同一content_type 中必须唯一")
        return codename
        
class UserAddForm(forms.Form):
    username = forms.CharField(required=True,min_length=3,error_messages={"required":"用户名不能为空","min_length":"用户名长度不能小于3位"})
    cn_name = forms.CharField(required=True,error_messages={"required":"中文名不能为空"})
    password = forms.CharField(required=True,min_length=8,error_messages={"required":"密码不能为空","min_length":"密码长度不能小于8位"})
    password_again = forms.CharField(required=True,min_length=8,error_messages={"required":"密码不能为空","min_length":"密码长度不能小于8位"})
    phone = forms.CharField(required=True,error_messages={"required":"手机号不能为空"})
    email = forms.EmailField(required=True,error_messages={"required":"邮箱不能为空","invalid":"邮箱格式错误"})


    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            user_obj = User.objects.get(username__exact=username)
        except User.DoesNotExist:
            return username
        except Exception as e:
            raise forms.ValidationError("%s" %(e.args))
        else:
            raise forms.ValidationError("该用户名%s已经存在,请更换其他用户名" %(username))

    def clean(self):
        cleaned_data = self.cleaned_data
        if self.is_valid():
            if cleaned_data.get('password') != cleaned_data.get('password_again'):
                raise forms.ValidationError("两次输入密码不一致,请重新输入")
            del cleaned_data['password_again']
            print("hhaa:",cleaned_data)
            return cleaned_data


class UserInfoChangePwdForm(forms.Form):
    password = forms.CharField(required=True,min_length=8,error_messages={"required":"密码不能为空","min_length":"密码长度不能小于8位"})
    password_again = forms.CharField(required=True,min_length=8,error_messages={"required":"密码不能为空","min_length":"密码长度不能小于8位"})

    def clean(self):
        cleaned_data = self.cleaned_data
        if self.is_valid():
            if cleaned_data.get('password') != cleaned_data.get('password_again'):
                raise forms.ValidationError("两次输入密码不一致,请重新输入")
            del cleaned_data['password_again']
            return cleaned_data

class UserInfoChangeForm(forms.Form):
    cn_name = forms.CharField(required=True,error_messages={"required":"中文名不能为空"})
    phone = forms.CharField(required=True,error_messages={"required":"手机号不能为空"})
    email = forms.EmailField(required=True,error_messages={"required":"邮箱不能为空","invalid":"邮箱格式错误"})

