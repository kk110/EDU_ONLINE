# _*_ coding: utf-8 _*_
__author__ = 'amy'
__date__ = '18-6-5 上午10:53'

import xadmin

from .models import UserAsk,CourseComment,UserFavorite,UserMessage,UserCourse


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name', 'add_time']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']


class CourseCommentAdmin(object):
    list_display = ['user__name', 'course__name', 'add_time']
    search_fields = ['user__name', 'course__name', 'add_time']
    list_filter = ['user__name', 'course__name', 'add_time']


class UserFavoriteAdmin(object):
    list_display = ['user__name', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user__name', 'fav_id', 'fav_type', 'add_time']
    list_filter = ['user__name', 'fav_id', 'fav_type', 'add_time']


class UserMessageAdmin(object):
    list_display = ['user', 'has_read', 'add_time']
    search_fields = ['user', 'has_read', 'add_time']
    list_filter = ['user', 'has_read', 'add_time']


class UserCourseAdmin(object):
    list_display = ['user__name', 'course__name', 'add_time']
    search_fields = ['user__name', 'course__name', 'add_time']
    list_filter = ['user__name', 'course__name', 'add_time']

xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComment, CourseCommentAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
