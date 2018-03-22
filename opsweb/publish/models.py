from django.db import models
from resources.models import CmdbModel,ServerModel
from django.contrib.auth.models import User

# Create your models here.

class PublishVersionModel(models.Model):
    STATUS_CHOICES = (
        ('running','当前运行的主版本'),
        ('run_pre','之前运行过的版本'),
        ('rollback','发生了回滚的版本'),
        ('packed','已经打包且未发布的版本'),
    )

    version = models.CharField("版本号",max_length=100,null=False,unique=True)
    status = models.CharField("版本状态",choices=STATUS_CHOICES,max_length=10,null=False,default='packed')
    pack_time = models.DateTimeField("打包时间",auto_now_add=True,null=True)
    module_name = models.ForeignKey(CmdbModel,verbose_name="模块名")
    jenkins_url = models.URLField("jenkins 地址",max_length=100,null=True)
    pack_user = models.CharField("打包人",max_length=50,null=True)

    def __str__(self):
        return "%s: %s" %(self.module_name,self.version)

    class Meta:
        verbose_name = "版本记录表"
        db_table = "publish_version"
        ordering = ["-id"]

class PublishHistoryModel(models.Model):
    STATUS_CHOICES = (
        ('success','成功'),
        ('failure','失败'),
    )

    TYPE_CHOICES = (
        ('publish','发布'),
        ('rollback','回滚'),
    )

    ENV_CHOICES = (
        ('online','生产'),
        ('gray','预发布'),
    )

    module_name = models.ForeignKey(CmdbModel,verbose_name="模块名")
    ip = models.ManyToManyField(ServerModel,verbose_name="模块的服务器IP地址")
    status = models.CharField("发布状态",choices=STATUS_CHOICES,max_length=10,null=True)
    env = models.CharField("环境",choices=ENV_CHOICES,max_length=10,null=True)
    type = models.CharField("类型",choices=TYPE_CHOICES,max_length=10,null=True)
    pub_time = models.DateTimeField("发布时间",auto_now_add=True,null=True)
    version_now = models.ForeignKey(PublishVersionModel,verbose_name="当前发布的版本号")
    pub_user = models.ForeignKey(User,verbose_name="发布人")
    pub_log_file = models.CharField("发布脚本执行日志",max_length=200,null=True)

    def __str__(self):
        return "%s-%s: %s" %(self.module_name,self.ip,self.version_now)

    class Meta:
        verbose_name = "发布历史表"
        db_table = "publish_history"
        ordering = ["-id"]
