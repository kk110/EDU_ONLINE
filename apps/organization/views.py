from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

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
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 城市筛选
        city_id = request.GET.get('city', '')
        print('-----cityid----')
        print(city_id)
        # 机构筛选
        category = request.GET.get('category', '')
        print('------category-----')
        print(category)
        # 排序依据
        sort = request.GET.get('sort')

        if city_id and category:
            all_orgs = CourseOrg.objects.filter(Q(city=city_id), Q(category=category))
        elif city_id:
            all_orgs = CourseOrg.objects.filter(city=city_id)
        elif category:
            all_orgs = CourseOrg.objects.filter(category=category)
        else:
            all_orgs = CourseOrg.objects.all()

        all_citys = CityDict.objects.all()
        org_nums = len(all_orgs)

        # 授课机构排名
        institutional_rankings = CourseOrg.objects.all().order_by('-click_nums')[:3]

        # 详情列表排序
        if sort == 'students':
            all_orgs = all_orgs.order_by('-student_nums')
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-class_nums')

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)

        params = {
            'all_citys': all_citys,
            'all_orgs': orgs,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'sort': sort,
            'institution_ranking': institutional_rankings,
        }
        return render(request, 'org-list.html', params)

    def post(self, request):
        pass
