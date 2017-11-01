from django.db import models

class People(models.Model):
    name = models.CharField("姓名",max_length=10,null=True)
    sex = models.CharField("性别",max_length=10,null=True)
    age = models.CharField("年龄",max_length=5,null=True)

    class Meta:
        db_table = "people"

class MobileTest(models.Model):
    number = models.CharField("手机号码",max_length=11,null=True)
    operator = models.CharField("运营商",max_length=20,null=True)
    provinces = models.CharField("所属省份",max_length=20,null=True)
    people_test = models.ForeignKey(People)

    class Meta:
        db_table = "mobile"
