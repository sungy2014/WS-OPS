import ldap
from dashboard.utils.get_ws_conf import get_myconf

def ldap_test(username,password):
    SERVER_NAME = '127.0.0.1'
    SERVER_PORT = 389
    ldap_conf = get_myconf(section="ldap_config")
    try:
        conn = ldap.open(SERVER_NAME, SERVER_PORT)
        #设置ldap协议版本
        conn.protocol_version = ldap.VERSION3
        # 设置验证的用户名，要以 dn 的方式，这里讲 username 中的 .号替换成空格 是因为 dn 中 CN 这个属性是使用空格
        # user = "CN=Haha Zhang, ......"
        user = "CN=%s," %(username.replace('.',' ')) + ldap_conf["mysec_conf"]["my_dn"]
        # 设置验证的密码
        pwd = password
        # 开始绑定，验证成功的话不会抛出异常
        conn.simple_bind_s(user,pwd)
    except ldap.LDAPError as e:
        print (e)
    else:
        print("ok")

if __name__ == '__main__':
    ldap_test('Haha.Zhang','12345678')
