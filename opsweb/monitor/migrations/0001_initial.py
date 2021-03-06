# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-01 15:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZabbixHostModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostid', models.CharField(db_index=True, max_length=10, unique=True, verbose_name='zabbix主机编号')),
                ('host', models.CharField(db_index=True, max_length=50, verbose_name='zabbix主机名')),
                ('status', models.CharField(choices=[('0', '监控中'), ('1', '未监控')], max_length=5, verbose_name='主机监控状态')),
                ('ip', models.GenericIPAddressField(db_index=True, protocol='IPv4', unique=True, verbose_name='监控的IP')),
                ('server', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='resources.ServerModel', verbose_name='关联到服务器表')),
            ],
            options={
                'db_table': 'zabbix_host',
                'ordering': ['ip'],
            },
        ),
    ]
