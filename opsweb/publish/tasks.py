from opsweb.celery import app
from dashboard.utils.ws_dingding import DingDingMsgSend
from dashboard.utils.ws_weixin import WxMsgSend

@app.task(name="dingding_msg_send")
def dingding_msg_send(data):
    dd = DingDingMsgSend()
    dd.send_dingding_link(data)

@app.task(name="wx_msg_send")
def wx_msg_send(data):
    WxMsgSend(data)
