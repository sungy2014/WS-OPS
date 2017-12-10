#!/usr/bin/env python
#coding=utf-8
'''
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
import json


accessKeyId = "LTAITtDdkCzVPspt"
accessSecret = "5wBDBhnbFS3l0dGMt9YgpGQuN08Txl"

clt = client.AcsClient(accessKeyId,accessSecret,'cn-hangzhou')

# 设置参数
request = DescribeInstancesRequest.DescribeInstancesRequest()
request.set_accept_format('json')

request.add_query_param('RegionId', 'cn-beijing')
request.add_query_param('ZoneId', 'cn-beijing-a')
request.add_query_param('PageSize', 50)

# 发起请求
response = clt.do_action_with_exception(request)

# 输出结果
print (type(response))
print ("*"*100)
print (json.dumps(json.loads(response)))
'''

from ansible_adhoc import ansible_adhoc
import json

server_info_data = ansible_adhoc('setup','gather_subset=hardware,!facter',"34")["172.17.134.34"]['ansible_facts']
print("*"*200)

server_refresh_info = {}
server_refresh_info['HostName'] = server_info_data['ansible_hostname']
server_refresh_info['OS'] = ' '.join((server_info_data['ansible_distribution'],server_info_data['ansible_distribution_version']))
server_refresh_info['ServerBrand'] = server_info_data['ansible_system_vendor']
server_refresh_info['ServerModel'] = server_info_data['ansible_product_name']
server_refresh_info['Kernel'] = server_info_data['ansible_kernel']
server_refresh_info['CpuCount'] = server_info_data['ansible_processor_vcpus']
server_refresh_info['CpuType'] = server_info_data["ansible_processor"][1]
server_refresh_info['RAM_GB'] = '%.2f GB' %(server_info_data['ansible_memtotal_mb']/1024.0)
server_refresh_info['SWAP_size'] = '%.2f GB' %(server_info_data['ansible_swaptotal_mb']/1024.0) 
server_refresh_info['PhyDiskSize'] = '\n'.join(['['+i+']'+':'+server_info_data['ansible_devices'][i]['size'] for i in server_info_data['ansible_devices'] if 'ss' in i or 'sd' in i or 'vd' in i]) 
server_refresh_info['Part_mount'] = '\n'.join(['['+i['mount']+']'+': %.2f GB' %(i['size_total']/1024.0/1024.0/1024.0) for i in server_info_data['ansible_mounts']])
print (server_refresh_info)
