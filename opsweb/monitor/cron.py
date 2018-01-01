from api.thirdapi import zabbix_api

def ZabbixHostSyncCrontab():
    zabbix_api.ZabbixHostAutoSync()    
