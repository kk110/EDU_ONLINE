from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.views.generic.base import View
from django.core.urlresolvers import reverse
from .models import UserProfile
from .forms import LoginForm,RegisterForm
from .tasks import hello_word,send_active_email
# Create your views here.

class CustomBackends(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

def index(request):
    return render(request, 'index.html')


def register(request):
    pass


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request, user)
                return render(request, 'index.html')
            elif user.is_active == 0:
                return render(request, 'login.html', {'message': '用户未激活'})
            else:
                return render(request, 'login.html', {'message': '用户名或密码错误！'})
        else:
            # return redirect(reverse('user:login'))
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = UserProfile()
            has_user = user.objects.filter(email=email)
            if has_user:
                return render(request, 'register.html', {'register_form':register_form, 'msg': '邮箱已存在'})
            user.email = email
            user.name = email
            user.password = make_password(password)
            user.is_active = False
            user.save()

            # 发送激活邮件

            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


def home(request):
    if request.method == "GET":
        # hello_word.delay()
        send_active_email.delay('klk_1115@163.com', 'register')
    return HttpResponse('测试celery')
