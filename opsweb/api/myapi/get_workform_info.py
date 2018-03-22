from workform.models import WorkFormModel,WorkFormTypeModel
from django.db.models import Count
from datetime import *


''' dashboard 中的工单统计 '''
class GetWorkFormInfo(object):
    time_interval = timedelta(days=7)
    seven_days_ago = date.today() - time_interval

    def get_workform_today_count(self):
        return WorkFormModel.objects.filter(create_time__gt=date.today()).count()
    
    def get_workform_count_by_type(self):
        wf_list = WorkFormTypeModel.objects.filter(workformmodel__create_time__gt=self.seven_days_ago).annotate(wf_count=Count("workformmodel")).exclude(wf_count__exact=0).values("cn_name","wf_count").order_by('-wf_count')
        return [{"name":i["cn_name"],"value":i["wf_count"]} for i in wf_list]
        
    def get_workform_count_by_reason(self):
        #sql_str = 'select id,reason as name,count(id) as value from workform where reason is not null GROUP BY reason;'
        #return [{"name":j,"value":i.value} for i in WorkFormModel.objects.raw(sql_str) for k,j in dict(WorkFormModel.REASON_CHOICES).items() if i.name==k]
        wf_reason_list = WorkFormModel.objects.filter(create_time__gt=self.seven_days_ago).exclude(reason__isnull=True).values("reason").annotate(value=Count("id")).order_by()
        return [{"name":j,"value":i.get("value")} for i in wf_reason_list for k,j in dict(WorkFormModel.REASON_CHOICES).items() if i.get("reason")==k]

    def get_workform_count_by_module(self):
        module_name_list = [ j for i in WorkFormModel.objects.filter(create_time__gt=self.seven_days_ago).exclude(module_name__isnull=True).values("module_name") for j in i.get("module_name").split(' -> ')]
        module_name_count = {}
        for mn in module_name_list:
            module_name_count[mn] = module_name_count.get(mn,0) + 1
        return sorted([{"name":k,"value":v} for k,v in module_name_count.items()],key=lambda x:x['value'],reverse=True)[:10]

