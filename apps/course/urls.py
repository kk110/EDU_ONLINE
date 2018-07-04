# _*_ coding: utf-8 _*_
__author__ = 'amy'
__date__ = '18-7-4 下午5:34'

from django.conf.urls import url
from .views import courseList,teacherList,orgList

urlpatterns = [
    url(r'course_list/$', courseList),
    url(r'teacher_list/$', teacherList),
    url(r'org_list/$', orgList),
]