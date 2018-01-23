from django import forms
from workform.models import WorkFormModel,ApprovalFormModel

class PubWorkFormAddForm(forms.Form):
    title = forms.CharField(required=True,max_length=100,error_messages={"required":"工单主题不能为空","max_length":"字符串长度必须小于100"})
    level = forms.ChoiceField(required=True,choices=WorkFormModel.LEVEL_CHOICES,error_messages={"required":"必须选择一个紧急程度"})
    detail = forms.CharField(required=True,max_length=800,error_messages={"required":"详情不能为空","max_length":"字符串长度必须小于800"})
    module_name = forms.CharField(required=True,max_length=500,error_messages={"required":"发布的模块不能为空","max_length":"字符串长度必须小于500"})
    sql = forms.ChoiceField(required=True,choices=WorkFormModel.SQL_CHOICES,error_messages={"required":"必须选择是否存在SQL"})
    sql_detail = forms.CharField(required=False,max_length=1000,error_messages={"max_length":"字符串长度必须小于1000"})
    sql_file_url = forms.CharField(required=False,max_length=1000,error_messages={"max_length":"上传了太多附件"})

    def clean_title(self):
        title = self.cleaned_data.get("title")
        try:
            wf_obj = WorkFormModel.objects.get(title__exact=title)
        except WorkFormModel.DoesNotExist:
            return title
        except Exception as e:
            raise forms.ValidationError(e.args)
        else:
            raise forms.ValidationError("该 title 的工单已经存在,请重新命名title")

    def clean(self):
        cleaned_data = self.cleaned_data
        if self.is_valid():
            if cleaned_data.get('sql') == 'yes':
                if cleaned_data.get('sql_detail') or cleaned_data.get('sql_file_url'):
                    return cleaned_data
                else:
                    raise forms.ValidationError("既然选择了'存在SQL',就必须填写'SQL详情'或者上传'SQL附件'")
            else:
                if cleaned_data.get('sql_detail') or cleaned_data.get('sql_file_url'):
                    raise forms.ValidationError("既然选择了'不存在SQL',就不能填写'SQL详情'或者上传'SQL附件'")
                else:
                    return cleaned_data
                

class WorkFormApprovalForm(forms.Form):
    result = forms.ChoiceField(required=True,choices=ApprovalFormModel.RESULT_CHOICES,error_messages={"required":"必须选择一个审批结果"})
    approve_note = forms.CharField(required=True,max_length=1000,error_messages={"required":"必须填写审批意见","max_length":"审批意见长度不能超过1000字符"})
