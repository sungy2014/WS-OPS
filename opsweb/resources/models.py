from django.db import models

# Create your models here.

class Server_IDC(models.Model):
    hostname = models.CharField("主机名",max_length=20,null=True)
    ssh_port = models.CharField("SSH 端口号",max_length=5,null=False,default="22")
    private_ip = models.GenericIPAddressField("私网IP",protocol="IPv4",unique=True,null=False)
    public_ip = models.GenericIPAddressField("公网IP",protocol="IPv4",null=True)
    env = models.CharField("所属环境:dev/test/online/ops",max_length=10,null=False)
    server_brand = models.CharField("服务器品牌",max_length=50,null=True)
    server_model = models.CharField("服务器型号",max_length=50,null=True)
    os_version = models.CharField("系统版本",max_length=50,null=True)
    cpu_type = models.CharField("CPU类型",max_length=50,null=True)
    cpu_count = models.DecimalField("CPU核数",max_digits=3,decimal_places=0,null=True)
    mem = models.CharField("内存大小",max_length=20,null=True)
    swap_size = models.CharField("SWAP 空间大小",max_length=10,null=True)
    disk_size = models.CharField("物理磁盘大小",max_length=50,null=True)
    part_mount = models.CharField("分区挂载情况",max_length=100,null=True)
    idc = models.CharField("归属机房",max_length=50,null=True)
    status = models.DecimalField("服务器状态:0-在线,1-下线",max_digits=1,decimal_places=0,null=False)
    online_time = models.DateTimeField("服务器上架时间",max_length=50,null=True)
    offline_time = models.DateTimeField("服务器下架时间",max_length=50,null=True)

    class Meta:
        db_table = "server_idc"
        ordering = ["private_ip"]


class IDC(models.Model):
    name = models.CharField("IDC 简称",max_length=10,null=False,unique=True)
    cn_name = models.CharField("IDC 中文名",max_length=100,null=False)
    address = models.CharField("IDC 地址",max_length=100,null=False)
    phone = models.CharField("IDC 联系电话",max_length=20,null=True)
    email = models.EmailField("IDC 邮箱",null=True)
    user = models.CharField("IDC 联系人",max_length=32,null=True)

    class Meta:
        db_table = "idc"
        permissions = (
            ("view_idc","查看idc列表"),
        )
