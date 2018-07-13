# _*_ coding: utf-8 _*_
__author__ = 'amy'
__date__ = '18-7-11 下午4:38'
from django.conf.urls import url
from django.views.static import serve
from EDU_ONLINE.settings import MEDIA_URL
from .views import CourseList, TeacherList, OrgList, AddUserAsk, OrgDetailList, OrgCourseList

urlpatterns = [
    url(r'course_list/$', CourseList.as_view(), name='courseList'),
    url(r'teacher_list/$', TeacherList.as_view(), name='teacherList'),
    url(r'org_list/$', OrgList.as_view(), name='orgList'),
    url(r'add_ask/$', AddUserAsk.as_view(), name='addAsk'),

    url(r'org_detail/(\d+)', OrgDetailList.as_view(), name='org_detail'),
    url(r'course_detail/(\d+)', OrgCourseList.as_view(), name='course_detail'),

    # 用于处理media文件下的图片
    url(r'media/(?P<path>.*)', serve, {'document_root': MEDIA_URL})
]