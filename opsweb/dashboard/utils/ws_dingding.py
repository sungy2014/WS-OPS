from dashboard.utils.get_ws_conf import get_myconf
from dashboard.utils.wslog import wslog_error,wslog_info
import  requests,json

dingding_conf = get_myconf(section="dingding_config")

if dingding_conf["result"] == 0:
    webhook = dingding_conf["mysec_conf"]["webhook"]
else:
    webhook = ''

def send_dingding(data):

    send_data = {"msgtype": "text", 
            "text": {
                "content": data
                }
            }

    headers = {'Content-Type': 'application/json'}

    r = requests.post(webhook,data=json.dumps(send_data),headers=headers)

    if int(json.loads(r.content)["errcode"]) == 0:
        wslog_info().info("钉钉机器人消息: '%s' 发送 成功" %(data))
    else:
        wslog_error().error("钉钉机器人消息: '%s' 发送失败,错误信息: %s" %(data,json.loads(r.content)["errmsg"]))

if __name__ == '__main__':
    send_dingding("哈哈，新年快乐")
