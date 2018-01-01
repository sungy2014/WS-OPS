from django.db import models
from resources.models import ServerModel

# Create your models here.

class ZabbixHostModel(models.Model):
    STATUS_CHOICES = (
        ("0","监控中"),
        ("1","未监控"),
    )

    hostid = models.CharField("zabbix主机编号",null=False,max_length=10,unique=True,db_index=True)
    host = models.CharField("zabbix主机名",null=False,max_length=50,db_index=True)
    status = models.CharField("主机监控状态",null=False,choices=STATUS_CHOICES,max_length=5)
    ip = models.GenericIPAddressField("监控的IP",protocol="IPv4",unique=True,null=False,db_index=True)
    server = models.OneToOneField(ServerModel,verbose_name="关联到服务器表")

    def __str__(self):
        return self.ip

    class Meta:
        db_table = "zabbix_host"
        ordering = ["ip"]
