# _*_ coding: utf-8 _*_
__author__ = 'amy'
__date__ = '18-6-5 上午10:54'
import xadmin

from .models import CityDict,CourseOrg,Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc']


class CourseOrgAdmin(object):
    list_display = ['name', 'click_nums', 'fav_nums', 'address', 'add_time','city']
    search_fields = ['name', 'click_nums', 'fav_nums', 'address', 'add_time', 'city']
    list_filter = ['name', 'click_nums', 'fav_nums', 'address', 'add_time', 'city__name']


class TeacherAdmin(object):
    list_style = ['name', 'work_years', 'position', 'work_company', 'points', 'click_nums','fav_nums','org__name']
    search_fields = ['name', 'work_years', 'position', 'work_company', 'points', 'click_nums', 'fav_nums', 'org__name','add_time']
    list_filter = ['name', 'work_years', 'position', 'work_company', 'points', 'click_nums', 'fav_nums', 'org__name']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)