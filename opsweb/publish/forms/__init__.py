from django import forms
from resources.models import CmdbModel,ServerModel
from publish.models import PublishVersionModel

class PublishPubForm(forms.Form):
    type = forms.CharField(required=True,error_messages={"required":"操作类型不能为空"})
    env = forms.CharField(required=True,error_messages={"required":"环境不能为空"})
    module_name = forms.CharField(required=True,error_messages={"required":"模块不能为空"})
    version = forms.CharField(required=True,error_messages={"required":"版本不能为空"})
    ip = forms.CharField(required=True,error_messages={"required":"服务器ip不能为空"})

    def clean_module_name(self):
        module_name_id = self.cleaned_data.get("module_name")
        try:
            m_obj = CmdbModel.objects.get(id__exact=module_name_id)
        except CmdbModel.DoesNotExist:
            raise forms.ValidationError("所选择的模块名不存在,请刷新重试")
        else:
            return m_obj

    def clean_version(self):
        version_id = self.cleaned_data.get("version")
        try:
            pv_obj = PublishVersionModel.objects.get(id__exact=version_id)
        except PublishVersionModel.DoesNotExist:
            raise forms.ValidationError("所选择的版本不存在,请刷新重试")
        else:
            return pv_obj
