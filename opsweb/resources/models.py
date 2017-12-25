from django.db import models

# Create your models here.


class IDC(models.Model):
    name = models.CharField("IDC 简称",max_length=20,null=False,unique=True)
    cn_name = models.CharField("IDC 中文名",max_length=100,null=False)
    address = models.CharField("IDC 地址",max_length=100,null=False)
    phone = models.CharField("IDC 联系电话",max_length=20,null=True)
    email = models.EmailField("IDC 邮箱",null=True)
    user = models.CharField("IDC 联系人",max_length=32,null=True)
    online_time = models.DateTimeField("IDC添加时间",auto_now_add=True,null=True)
    last_update_time = models.DateTimeField("最后一次更新时间",auto_now=True,null=True)

    def __str__(self):
        return "%s-%s" %(self.name,self.cn_name)

    class Meta:
        db_table = "idc"
        permissions = (
            ("view_idc","查看idc列表"),
        )

class ServerIdcModel(models.Model):

    ENV_CHOICES = (
        ("dev",u"开发"),
        ("test",u"测试"),
        ("online",u"生产"),
        ("ops",u"运维"),
    )

    STATUS_CHOICES = (
        ("Running",u"运行中"),
        ("Starting",u"启动中"),
        ("Stopping",u"停止中"),
        ("Stopped",u"已停止"),
    )

    MONITOR_CHOICES = (
        ("0",u"正常"),
        ("1",u"未监控"),
    )


    hostname = models.CharField("主机名",max_length=20,null=True)
    ssh_port = models.CharField("SSH 端口号",max_length=5,null=False,default="22")
    private_ip = models.GenericIPAddressField("私网IP",protocol="IPv4",unique=True,null=False)
    public_ip = models.GenericIPAddressField("公网IP",protocol="IPv4",null=True)
    env = models.CharField("所属环境",choices=ENV_CHOICES,max_length=10,null=False,default="online") 
    server_brand = models.CharField("服务器品牌",max_length=50,null=True)
    server_model = models.CharField("服务器型号",max_length=50,null=True)
    os_version = models.CharField("系统版本",max_length=50,null=True)
    cpu_type = models.CharField("CPU类型",max_length=50,null=True)
    cpu_count = models.CharField("CPU核数",max_length=10,null=True)
    mem = models.CharField("内存大小",max_length=20,null=True)
    swap = models.CharField("SWAP 空间大小",max_length=10,null=True)
    disk = models.CharField("物理磁盘大小",max_length=200,null=True)
    disk_mount = models.CharField("分区挂载情况",max_length=100,null=True)
    sn_code = models.CharField("服务器SN号",max_length=20,null=True,unique=True)
    cabinet_num = models.CharField("机柜编号",max_length=50,null=True)
    idc = models.ForeignKey(IDC,verbose_name="归属机房")
    status = models.CharField("服务器状态",choices=STATUS_CHOICES,max_length=10,null=True) 
    monitor_status = models.CharField("服务器监控状态",choices=MONITOR_CHOICES,max_length=10,null=True) 
    online_time = models.DateTimeField("服务器上架时间",auto_now_add=True,null=True)
    offline_time = models.DateTimeField("服务器下架时间",max_length=50,null=True)
    expired_time = models.DateTimeField("服务器过保时间",null=True)
    last_update_time = models.DateTimeField("最后一次更新时间",auto_now=True,null=True)

    def __str__(self):
        return "%s-%s" %(self.hostname,self.private_ip)

    class Meta:
        db_table = "server_idc"
        ordering = ["private_ip"]

class ServerAliyunModel(models.Model):

    ENV_CHOICES = (
        ("dev",u"开发"),
        ("test",u"测试"),
        ("online",u"生产"),
        ("ops",u"运维"),
        ("gray",u"预发布"),
    )

    STATUS_CHOICES = (
        ("Running",u"运行中"),
        ("Starting",u"启动中"),
        ("Stopping",u"停止中"),
        ("Stopped",u"已停止"),
    )

    MONITOR_CHOICES = (
        ("0",u"正常"),
        ("1",u"未监控"),
    )

    CHARGE_TYPE_CHOICES = ( 
        ("PrePaid",u"包年包月"),
        ("PostPaid",u"按量付费"),
    )

    RENEWLI_STATUS_CHOICES = (
        ("AutoRenewal","自动续费"),
        ("Normal","手动续费"),
        ("NotRenewal","不在续费"),
        ("RenewalByUsed","按量付费"),
    )

    hostname = models.CharField("主机名",max_length=50,null=True)
    ssh_port = models.CharField("SSH 端口号",max_length=5,null=False,default="22")
    private_ip = models.GenericIPAddressField("私网IP",protocol="IPv4",unique=True,null=True,db_index=True)
    public_ip = models.GenericIPAddressField("公网IP",protocol="IPv4",null=True)
    instance_id = models.CharField("实例ID",max_length=50,unique=True,null=True,db_index=True)
    env = models.CharField("所属环境",choices=ENV_CHOICES,max_length=10,null=False,default="online")
    server_brand = models.CharField("服务器品牌",max_length=50,null=True)
    os_version = models.CharField("系统版本",max_length=50,null=True)
    cpu_count = models.CharField("CPU核数",max_length=10,null=True)
    mem = models.CharField("内存大小",max_length=20,null=True)
    swap = models.CharField("SWAP 空间大小",max_length=10,null=True)
    disk = models.CharField("物理磁盘大小",max_length=200,null=True)
    disk_mount = models.CharField("分区挂载情况",max_length=100,null=True)
    instance_type = models.CharField("实例规格",max_length=50,null=True)
    charge_type = models.CharField("付费类型",choices=CHARGE_TYPE_CHOICES,max_length=10,null=True)
    renewal_type = models.CharField("续费类型",choices=RENEWLI_STATUS_CHOICES,max_length=50,null=True)
    region = models.CharField("地域",max_length=50,null=True)
    zone = models.CharField("可用区",max_length=50,null=True)
    status = models.CharField("服务器状态",choices=STATUS_CHOICES,max_length=10,null=True)
    monitor_status = models.CharField("服务器监控状态",choices=MONITOR_CHOICES,max_length=10,null=True)
    online_time = models.DateTimeField("服务器上架时间",auto_now_add=False,null=True)
    offline_time = models.DateTimeField("服务器下架时间",null=True)
    expired_time = models.DateTimeField("服务器过期时间",null=True)
    last_update_time = models.DateTimeField("最后一次更新时间",auto_now=True,null=True)

    def __str__(self):
        return "%s-%s" %(self.hostname,self.private_ip)

    class Meta:
        db_table = "server_aliyun"
        ordering = ["private_ip"]

class CmdbModel(models.Model):

    WAY_CHOICES = (
        ('0',"tomcat"),
        ('1','jar'),
        ('3','node'),
        ('4','php'),
        ('5','其他'),
    )

    STATUS_CHOICES = (
        ('0','运行中'),
        ('1','待上线'),
        ('2','已停服'),
    )

    ENV_CHOICES = (
        ("dev",u"开发"),
        ("test",u"测试"),
        ("online",u"生产"),
        ("ops",u"运维"),
        ("gray",u"预发布"),
    )

    TYPE_CHOICES = (
        ("0","核心应用"),
        ("1","一般应用"),
        ("2","中间件"),
        ("3","其他"),
    )

    name = models.CharField("应用名",max_length=50,null=False,unique=True)
    ips = models.ManyToManyField(ServerAliyunModel,verbose_name="IP 地址")
    env = models.CharField("所属环境",choices=ENV_CHOICES,max_length=10,null=False,default="online")
    describe = models.CharField("对应用的简单描述",max_length=200,null=True)
    path = models.CharField("应用部署的路径",max_length=200,null=True)
    script = models.CharField("应用启动脚本",max_length=200,null=True)
    log = models.CharField("应用日志路径",max_length=200,null=True)
    ports = models.CharField("应用打开的端口",max_length=200,null=True)
    way = models.CharField("部署方式",max_length=10,choices=WAY_CHOICES,null=True)
    type = models.CharField("应用类型",max_length=10,choices=TYPE_CHOICES,null=True)
    status = models.CharField("应用状态",choices=STATUS_CHOICES,max_length=10,null=True)
    online_time = models.DateTimeField("应用上架时间",auto_now_add=True,null=True)
    offline_time = models.DateTimeField("应用下线时间",null=True)
    last_update_time = models.DateTimeField("应用最后更新时间",auto_now=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cmdb'
        ordering = ['name']

class ServerStatisticByDayModel(models.Model):
    myday = models.DateField("统计时间",null=False,unique=True)
    count = models.PositiveSmallIntegerField("服务器数量",null=False)
    compared_with_yesterday = models.CharField("与昨日相比变化的数量",max_length=5,null=False,default='0')
    last_update_time = models.DateTimeField("应用最后更新时间",auto_now=True,null=True)

    def __str__(self):
        return self.myday

    class Meta:
        db_table = 'server_statistic_by_day'
        ordering = ['myday']

class CmdbStatisticByDayModel(models.Model):
    myday = models.DateField("统计时间",null=False,unique=True)
    count = models.PositiveSmallIntegerField("应用数量",null=False)
    compared_with_yesterday = models.CharField("与昨日相比变化的数量",max_length=5,null=False,default='0')
    last_update_time = models.DateTimeField("应用最后更新时间",auto_now=True,null=True)

    def __str__(self):
        return self.myday

    class Meta:
        db_table = 'cmdb_statistic_by_day'
        ordering = ['myday']
