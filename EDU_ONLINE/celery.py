# _*_ coding: utf-8 _*_
__author__ = 'amy'
__date__ = '18-6-14 下午5:20'

import os
import django

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EDU_ONLINE.settings')
django.setup()

app = Celery('EDU_ONLINE')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)