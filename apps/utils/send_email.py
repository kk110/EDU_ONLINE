# _*_ coding: utf-8 _*_
__author__ = 'amy'
__date__ = '18-6-13 下午6:02'

import random
from django.conf import settings
from django.core.mail import send_mail
from users.models import EmailVerifyRecord

def create_random_code(codelen):
    active_code = ''
    ran_str = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    for _ in range(codelen):
        flag = random.randint(len(ran_str))
        active_code += ran_str[flag]
    return  active_code


def send_active_mail(receive_email, send_type):
    if send_type == "register":
        sender = settings.EMAIL_HOST_USER
        active_code = create_random_code(18)
        send_code = """<a>""" + active_code + """</a>"""
        email_title = '欢迎注册慕学网'
        email_content = '点击下方链接激活您的账户:' + send_code
        send_status = send_mail(email_title, email_content, sender, [receive_email])
        if send_status == 1:
            record = EmailVerifyRecord()
            record.code = active_code
            record.email = receive_email
            record.send_type = send_type
        return  send_status


