from django import template
from workform.models import ProcessModel

register = template.Library()

@register.filter(name="get_process_step")
def get_process_step(value):

    if not value:
        return "None"
    
    process_step_list = value.split(" -> ")
    pricess_step_name_list = []

    for step_id  in process_step_list:
        try:
            pm_obj = ProcessModel.objects.get(step_id__exact=step_id)
        except:
            pricess_step_name_list.append('None')
        else:
            pricess_step_name_list.append(pm_obj.step)

    return ' -> '.join(pricess_step_name_list)
            
        
