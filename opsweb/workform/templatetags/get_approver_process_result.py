from django import template

register = template.Library()

@register.filter(name="get_approver_result")
def get_approver(value):
    a_obj = value.approvalformmodel_set.exclude(result__exact=None).order_by("-id")[0]

    approver =  a_obj.approver.userextend.cn_name

    if a_obj.result == "1":
        process_result = '<span style="color:red">%s</span>' %(a_obj.get_result_display())
    elif a_obj.result == "2":
        process_result = '<span style="color:yellow">%s</span>' %(a_obj.get_result_display())
    elif a_obj.result == "3":
        process_result = '<span style="color:red">%s</span>' %(a_obj.get_result_display())
    else:
        process_result = '<span>%s</span>' %(a_obj.get_result_display())

    return "%s</br>%s" %(approver,process_result)

