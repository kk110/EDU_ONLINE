# _*_ coding: utf-8 _*_
__author__ = 'amy'
__date__ = '18-6-14 下午5:23'

from EDU_ONLINE.celery import app
from utils.send_email import send_register_active_email
import time

@app.task
def hello_word():
    print('hello world,------')

@app.task
def send_asyn_active_email(to_email, send_type, u_id):
    task_status = send_register_active_email(to_email, send_type, u_id)
    return task_status