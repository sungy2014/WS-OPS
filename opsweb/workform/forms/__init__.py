from django import forms
from django.forms import ModelForm
from workform.models import WorkFormModel,ApprovalFormModel,WorkFormTypeModel

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

class WorkFormTypeAddForm(ModelForm):
    class Meta:
        model = WorkFormTypeModel
        fields = ["name","cn_name","process_step_id"]
        error_messages = {
            "name" : {
                "required": "必须填写名称",
                "max_length": "名称长度不能超过50字符",
            },
            "cn_name" : {
                "required": "必须填写中文名",
                "max_length": "中文名长度不能超过200字符",
            },
            "process_step_id" : {
                "required": "必须选择此工单类型的流程",
                "max_length": "流程不能超过500字符",
            },
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        try:
            wft_obj = WorkFormTypeModel.objects.get(name__exact=name)
        except WorkFormTypeModel.DoesNotExist:
            return name
        else:
            raise forms.ValidationError("该名称已经存在")

    def clean_cn_name(self):
        cn_name = self.cleaned_data.get("cn_name")
        try:
            wft_obj = WorkFormTypeModel.objects.get(cn_name__exact=cn_name)
        except WorkFormTypeModel.DoesNotExist:
            return cn_name
        else:
            raise forms.ValidationError("该中文名已经存在") 

    def clean_process_step_id(self):
        process_step_id = self.cleaned_data.get("process_step_id")
        process_step_list = process_step_id.split(' -> ')
        # 判断最后一个流程步骤有没有选择 "完成"
        if process_step_list[-1] != "60":
            raise forms.ValidationError("流程步骤必须以 '完成' 结束")
        else:
            return process_step_id

class WorkFormTypeChangeForm(WorkFormTypeAddForm):
    class Meta(WorkFormTypeAddForm.Meta):
        exclude = ["name","cn_name"]
