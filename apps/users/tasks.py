# _*_ coding: utf-8 _*_
__author__ = 'amy'
__date__ = '18-6-14 下午5:23'

from django.core.mail import send_mail
from django.conf import settings
from EDU_ONLINE.celery import app
# from utils.send_email import send_mails
import time

@app.task
def hello_word():
    print('hello world,------')

@app.task
def send_active_email(receive_email, send_type):
    if send_type == 'register':
        sender = settings.EMAIL_FROM
        active_code = 'welcome'
        subject = '欢迎注册慕学网'
        message = ''
        receiver = [receive_email]
        email_content = "<h1>点击下方链接激活您的账户:<a href='%s'>http://192.168.136.128:8000/active/%s</a></h1>" % (
        active_code, active_code)
        send_status = send_mail(subject, message, sender, receiver, html_message=email_content)
        print("=====send_mail====")
        print(send_status)
        # send_mails(receive_email, send_type)
        time.sleep(5)