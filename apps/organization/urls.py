# _*_ coding: utf-8 _*_
__author__ = 'amy'
__date__ = '18-7-11 下午4:38'
from django.conf.urls import url
from django.views.static import serve
from EDU_ONLINE.settings import MEDIA_URL
from .views import courseList, teacherList, orgList, addUserAsk

urlpatterns = [
    url(r'^course_list/$', courseList.as_view(), name='courseList'),
    url(r'^teacher_list/$', teacherList.as_view(), name='teacherList'),
    url(r'^org_list/$', orgList.as_view(), name='orgList'),
    url(r'^add_ask/$', addUserAsk.as_view(), name='addAsk'),

    # 用于处理media文件下的图片
    url(r'media/(?P<path>.*)', serve, {'document_root': MEDIA_URL})
]