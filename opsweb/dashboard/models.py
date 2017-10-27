from django.db import models

# Create your models here.

class Test(models.Model):
    username = models.CharField(max_length=20,null=False,default="haha",verbose_name="用户名")
