from opsweb.celery import app
from dashboard.utils.ws_mail_send import mail_send

@app.task(name="workform_mail_send")
def workform_mail_send(subject,message,mail_to,html_content=None):
    mail_send(subject, message, mail_to, html_content=html_content)
