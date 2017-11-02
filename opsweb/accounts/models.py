from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserExtend(models.Model):
    user = models.OneToOneField(User,verbose_name="扩展用户表,与用户模型User建立一对一关系")
    cn_name = models.CharField("中文名",max_length=50,null=False)
    phone = models.CharField("手机号",max_length=11,null=False)

    class Meta:
        db_table = "user_extend"
    
