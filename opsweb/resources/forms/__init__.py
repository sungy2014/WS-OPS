from django import forms
from resources.models import IDC


class IdcAddForm(forms.Form):
    name = forms.CharField(required=True,error_messages={"invalid":"简称不能为空"})
    cn_name = forms.CharField(required=True,error_messages={"invalid":"中文名不能为空"})
    user = forms.CharField(required=True,error_messages={"invalid":"联系人不能为空"})
    phone = forms.CharField(required=True,error_messages={"invalid":"电话不能为空"})
    email = forms.EmailField(required=False)
    address = forms.CharField(required=True,error_messages={"invalid":"地址不能为空"})

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
