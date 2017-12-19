from django import forms
from resources.models import IDC,ServerAliyunModel,CmdbModel


class IdcAddForm(forms.Form):
    name = forms.CharField(required=True,error_messages={"required":"简称不能为空"})
    cn_name = forms.CharField(required=True,error_messages={"required":"中文名不能为空"})
    user = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    address = forms.CharField(required=True,error_messages={"required":"地址不能为空"})

    def clean_name(self):
        name = self.cleaned_data.get("name")
        try:
            IDC.objects.get(name__exact=name)
        except IDC.DoesNotExist:
            return name
        except Exception as e:
            raise forms.ValidationError(e.args)
        else:
            raise forms.ValidationError("IDC 简称已经存在")

class IdcChangeForm(forms.Form):
    user = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    address = forms.CharField(required=True,error_messages={"required":"地址不能为空"})

class ServerAliyunAddForm(forms.Form):
    private_ip = forms.GenericIPAddressField(required=True,protocol="IPv4",error_messages={"required":"IP地址不能为空","invalid":"IPv4地址无效"})
    ssh_port = forms.CharField(required=True,max_length=5,error_messages={"required":"SSH端口不能为空","max_length":"SSH端口不能超过5位数字"})
    env = forms.ChoiceField(required=True,choices=ServerAliyunModel.ENV_CHOICES,error_messages={"required":"必须选择一个环境"})

    def clean_private_ip(self):
        private_ip = self.cleaned_data.get("private_ip")
        try:
            server_aliyun_obj = ServerAliyunModel.objects.get(private_ip__exact=str(private_ip))
        except ServerAliyunModel.DoesNotExist:
            return private_ip
        except Exception as e:
            raise forms.ValidationError(e.args)
        else:
            raise forms.ValidationError("该IP已经存在，不需要添加")

    def clean_ssh_port(self):
        ssh_port = self.cleaned_data.get("ssh_port")
        if int(ssh_port) >= 65535:
            raise forms.ValidationError("SSH端口必须小于65535")
        return ssh_port

class ServerAliyunUpdateForm(forms.Form):
    public_ip = forms.GenericIPAddressField(required=False,protocol="IPv4",error_messages={"invalid":"IPv4地址无效"})
    ssh_port = forms.CharField(required=True,max_length=5,error_messages={"required":"SSH端口不能为空","max_length":"SSH端口不能超过5位数字"})
    hostname = forms.CharField(required=False,max_length=20,error_messages={"max_length":"主机名不能超过20字符"})
    env = forms.ChoiceField(required=True,choices=ServerAliyunModel.ENV_CHOICES,error_messages={"required":"必须选择一个环境"})

    def clean_ssh_port(self):
        ssh_port = self.cleaned_data.get("ssh_port")
        if int(ssh_port) >= 65535:
            raise forms.ValidationError("SSH端口必须小于65535")
        return ssh_port


class ServerIdcAddForm(forms.Form):
    idc = forms.IntegerField(required=True)

    def clean_idc(self):
        idc_id = self.cleaned_data.get("idc")
        try:
            idc_obj = IDC.objects.get(id__exact=int(idc_id))
        except IDC.DoesNotExist:
            raise forms.ValidationError("IDC 不存在")
        else:
            return idc_obj

class CmdbAddForm(forms.Form):
    name = forms.CharField(required=True,max_length=50,error_messages={"required":"应用名称不能为空","max_length":"应用名称不能超过50字符"})
    describe = forms.CharField(required=False,max_length=200,error_messages={"invalid":"这个字段的值无效","max_length":"不允许超过200字符"})
    path = forms.CharField(required=True,max_length=200,error_messages={"invalid":"这个字段的值无效","max_length":"不允许超过200字符"})
    script = forms.CharField(required=True,max_length=200,error_messages={"invalid":"这个字段的值无效","max_length":"不允许超过200字符"})
    type = forms.ChoiceField(required=True,choices=CmdbModel.TYPE_CHOICES,error_messages={"required":"必须选择一个类型"})
    log = forms.CharField(required=False,max_length=200,error_messages={"invalid":"这个字段的值无效","max_length":"不允许超过200字符"})
    ports = forms.CharField(required=False,max_length=200,error_messages={"invalid":"这个字段的值无效","max_length":"不允许超过200字符"})
    status = forms.ChoiceField(required=True,choices=CmdbModel.STATUS_CHOICES,error_messages={"required":"必须选择一个状态"})


    def clean__name(self):
        name = self.cleaned_data.get("name")
        try:
            cmdb_obj = CmdbModel.objects.get(name__exact=name)
        except CmdbModel.DoesNotExist:
            return name
        else:
            raise forms.ValidationError("应用名称已经存在，请重新定义应用名称")

