import  re

from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views.generic.base import View
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg,Teacher,CityDict
from operation.models import UserAsk
from .forms import UserAskForm

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


# 授课机构列表展示
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


# 授课机构页表单提交
class addUserAsk(View):
    def post(self, request):
        # 此处form 验证有问题
        # askForm = UserAskForm()
        # if askForm.is_valid():
        #     uses_ask = askForm.save(commit=True)
        #     data = {
        #         'status': 'success',
        #     }
        #     return JsonResponse(data)
        # else:
        #     data = {
        #         'status': 'fail',
        #         'msg': askForm.errors,
        #     }
        #     print(askForm.errors)
        #     return JsonResponse(data)
        name = request.POST.get('name', '')
        mobile = request.POST.get('mobile', '')
        course_name = request.POST.get('course_name', '')

        if not all([name, mobile, course_name]):
            data = {
                'status': 'fail',
                'msg': '以上三项不能为空！'
            }
            return JsonResponse(data)

        name_pattern = re.compile(r'\w{2,20}')
        name_result = name_pattern.match(name)
        if not name_result:
            data = {
                'status': 'fail',
                'msg': '名字长度为2-20的汉字  '
            }
            return JsonResponse(data)

        mobile_pattern = re.compile(r'^\d{11}$')
        mobile_result = mobile_pattern.match(mobile)
        if not mobile_result:
            data = {
                'status': 'fail',
                'msg': '手机号码必须为11位的纯数字！'
            }
            return JsonResponse(data)

        course_pattern = re.compile(r'^\w{1,50}$')
        course_result = course_pattern.match(mobile)
        if not course_result:
            data = {
                'status': 'fail',
                'msg': '课程名应在50字以内！'
            }
            return JsonResponse(data)

        ask = UserAsk()
        ask.name = name
        ask.course_name = course_name
        ask.mobile = mobile
        ask.save()
        data = {
            'status': 'success'
        }
        return JsonResponse(data)