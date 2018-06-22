# _*_ coding: utf-8 _*_
__author__ = 'amy'
__date__ = '18-6-8 上午10:21'
from django.conf.urls import url
from .views import index, LoginView, RegisterView, ActiveEmailView, reActiveEmail, ForgetPassword, ResetPassword

urlpatterns = [
    url(r'^index/$', index, name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^user/active/(?P<code>.*)/$', ActiveEmailView.as_view(), name='active'),
    url(r'^resend_email/$', reActiveEmail, name='reactive'),
    url(r'^forget/$', ForgetPassword.as_view(), name='forget_pwd'),
    # url(r'^forget/$', find_page),
    url(r'^reset_password/$', ResetPassword.as_view(), name='reset'),
    # url(r'^my_mail/$', myMail)
]