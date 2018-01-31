from django import template

register = template.Library()

@register.filter(name="get_approver_result")
def get_approver(value):

    a_list = value.approvalformmodel_set.exclude(result__exact=None).order_by("-id")

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

