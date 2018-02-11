#!/usr/bin/env python
#coding=utf-8
import ldap

class ldap_xin():
    def __init__(self, ldap_who, ldap_cred):
        self.ldap_host = "192.168.1.2"
        self.ldap_port = 389
        self.ldap_who = "bbb" + "\\" + ldap_who
        self.ldap_cred = ldap_cred
        self.ldap_baseondn = "OU=AAA,DC=bbb,DC=ccc,DC=ddd"
        self.filterwd = 'samaccountname=' + ldap_who + '*'
        self.ret = {}
    def check(self):
        # 连接ldap
        l = ldap.open(self.ldap_host, self.ldap_port)
        try:
            l.simple_bind_s(self.ldap_who, self.ldap_cred)
        except ldap.INVALID_CREDENTIALS:
            self.ret["authcode"] = -1
            return self.ret
        result_id = l.search(self.ldap_baseondn, ldap.SCOPE_SUBTREE, self.filterwd, None)
        try:
            result_type, result_data = l.result(result_id, 0)
        except ldap.OPERATIONS_ERROR:
            self.ret["authcode"] = -1
            return self.ret
        self.ret["authcode"] = 1
        return self.ret

#调用:
#test1 = ldap_xin('username', 'password')  # ldap用户的账号密码
#print test1.check()

