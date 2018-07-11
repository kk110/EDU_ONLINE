from django.shortcuts import render
from django.views.generic.base import View

from .models import CourseOrg,Teacher,CityDict

# Create your views here.


class courseList(View):
    def get(self, request):

        return render(request, 'course-list.html')

    def post(self, request):
        pass


class teacherList(View):
    def get(self, request):
        return render(request, 'teachers-list.html')

    def post(self, request):
        pass


class orgList(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        params = {
            'all_citys': all_citys,
            'all_orgs': all_orgs,
        }
        return render(request, 'org-list.html',params)

    def post(self, request):
        pass
