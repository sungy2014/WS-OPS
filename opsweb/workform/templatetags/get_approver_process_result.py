from django import template
from django.db.models import Q


register = template.Library()

@register.filter(name="get_approver_result")
def get_approver(value):

    ''' 过滤掉审核结果为空,以及 流程step 为'完成' 状态的工单审核对象 '''
    a_list = value.approvalformmodel_set.exclude(Q(result__exact=None)|Q(process_id__exact=6)).order_by("-id")

    if not a_list:
        return "None</br>None"

    a_obj = a_list[0]

    approver =  a_obj.approver.userextend.cn_name

    if a_obj.result == "1":
        process_result = '<span style="background-color: red;color: #FFFFFF;">%s</span>' %(a_obj.get_result_display())
    elif a_obj.result == "2":
        process_result = '<span style="background-color: #f8ac59;color: #FFFFFF;">%s</span>' %(a_obj.get_result_display())
    elif a_obj.result == "3":
        process_result = '<span style="background-color: red;color: #FFFFFF;">%s</span>' %(a_obj.get_result_display())
    else:
        process_result = '<span style="background-color: #21b9bb;color: #FFFFFF;">%s</span>' %(a_obj.get_result_display())

    return "%s</br>%s" %(approver,process_result)

