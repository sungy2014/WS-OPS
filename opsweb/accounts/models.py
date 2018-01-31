from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserExtend(models.Model):
    ROLE_CHOICES = (
        ("0","Head"),
        ("1","Controller"),
        ("2","Manager"),
        ("3","Pmin"),
    )

    user = models.OneToOneField(User,verbose_name="扩展用户表,与用户模型User建立一对一关系")
    cn_name = models.CharField("中文名",max_length=50,null=False)
    role = models.CharField("角色",choices=ROLE_CHOICES,max_length=10,null=False,default="1")
    phone = models.CharField("手机号",max_length=11,null=False)
    last_change_time = models.DateTimeField("最后修改时间",auto_now=True)

    def __str__(self):
        return self.cn_name

    class Meta:
        verbose_name = "扩展用户表"
        db_table = "user_extend"
    
