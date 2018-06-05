# _*_ coding: utf-8 _*_
__author__ = 'amy'
__date__ = '18-6-5 上午9:35'

import xadmin

from .models import Course,Lesson,Video,CourseResource


class CourseAdmin(object):
    list_display = ['name', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_num', 'add_time']
    search_fields = ['name', 'desc', 'degree', 'fav_nums', 'click_num', 'add_time']
    list_filter = ['name', 'degree', 'students', 'fav_nums', 'click_num']


class LessonAdmin(object):
    list_play = ['name', 'course__name', 'add_time']
    seach_fields = ['course__name', 'name', 'add_time']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_play = ['name', 'lesson', 'add_time']
    search_fields = ['name', 'lesson']
    list_filter = ['name', 'lesson__name', 'add_time']


class CourseResourceAdmin(object):
    list_play = ['course', 'name', 'add_time', 'download']
    search_fields = ['course', 'name', 'add_time']
    list_filter = ['name', 'course__name', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)