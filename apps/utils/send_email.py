# _*_ coding: utf-8 _*_
__author__ = 'amy'
__date__ = '18-6-13 下午6:02'

from django_redis import get_redis_connection
import random
from django.conf import settings
from django.core.mail import send_mail
import time
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from users.models import EmailVerifyRecord


def create_random_code(codelen):
    active_code = ''
    ran_str = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    for _ in range(codelen):
        flag = random.randint(0, len(ran_str)-1)
        active_code += ran_str[flag]
    return active_code


# def send_my_mails(receive_email, send_type):
#     if send_type == "register":
#         sender = settings.EMAIL_FROM
#         active_code = create_random_code(18)
#         subject = '欢迎注册慕学网'
#         message = ''
#         html_message = "<h1>点击下方链接激活您的账户:<a href='%s'>http://192.168.136.128:8000/active/%s</a></h1>"%(active_code,active_code)
#         receiver = [receive_email]
#         send_status = send_mail(subject, message, sender, receiver, html_message=html_message)
#         # if send_status == 1:
#         #     record = EmailVerifyRecord()
#         #     record.code = active_code
#         #     record.email = receive_email
#         #     record.send_type = send_type
#         # return send_status
#         print("====active code====")
#         print(active_code)
#         return send_status


def send_register_active_email(to_email, send_type, u_id):
    if send_type == 'register':
        '''发送激活邮件'''
        email_title = '慕学在线网欢迎信息'
        email_body = ''
        sender = settings.EMAIL_HOST_USER
        receiver = [to_email]
        active_code = create_random_code(15)

        # 加密激活码和user_id
        serializer = Serializer(settings.SECRET_KEY)
        info = {'confirm': active_code + str(u_id)}  # 注意需要str类型
        token = serializer.dumps(info)  # bytes
        token = token.decode()
        html_message = '<h1>hello, 欢迎您成为慕学在线网学员</h1>请点击下面链接激活您的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (token, token)

        # 发邮件
        send_status = send_mail(email_title, email_body, sender, receiver, html_message=html_message)
        print("====发邮件ing=====")
        print(send_status)
        # 模拟邮件发送了5s
        time.sleep(2)
        if send_status == 1:
            print("=====saving=====")
            record = EmailVerifyRecord()
            record.email = to_email
            record.send_type = send_type
            record.code = token
            record.which_user = str(u_id)
            record.save()

            # 使用redis存储激活码，类型hash,格式register id code
            # conn = get_redis_connection('default')
            # conn.hset('register', u_id, token)
            # conn.expire('register', 3600)       # timeout 3600s
            return 1


