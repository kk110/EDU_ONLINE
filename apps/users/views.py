from django_redis import get_redis_connection
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.views.generic.base import View
from django.core.urlresolvers import reverse
from django.conf import settings
import re
from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, FindPasswordForm,ForgetForm
from .tasks import hello_word, send_asyn_active_email
# from utils import send_email

# Create your views here.
conn = get_redis_connection('default')

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
                if user.is_active == 0:
                    return render(request, 'login.html', {'message': '用户未激活,请前往邮箱激活'})
                else:
                    login(request, user)
                    return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'message': '用户名或密码错误！'})
        else:
            # return redirect(reverse('user:login'))
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_profile = UserProfile()
            has_user = UserProfile.objects.filter(email=email)
            if has_user:
                return render(request, 'register.html', {'register_form': register_form, 'msg': '邮箱已存在'})
            user_profile.email = email
            user_profile.username = email
            user_profile.password = make_password(password)
            user_profile.is_active = False
            user_profile.save()

            # 发送激活邮件
            send_type = 'register'
            # status = send_email.send_register_active_email(email, send_type, user_profile.id)
            status = send_asyn_active_email.delay(email, send_type, user_profile.id)
            print('---user id -----')
            print(user_profile.id)
            print('----status----')
            print(status)
            key_name = "celery-task-meta-" + str(status)
            conn = get_redis_connection('result')
            result = conn.get(key_name)
            # if result is None:
            success = 'SUCCESS'.encode()
            if success in result:
                return render(request, 'login.html', {'register_form': register_form})
            else:
                return render(request, 'register.html', {'register_form': register_form, 'msg': '邮件发送失败'})
        else:
            return render(request, 'register.html', {'register_form': register_form})


# 用户激活
class ActiveEmailView(View):
    def get(self, request, code):
        # 解密激活链接或取id和激活码
        serializer = Serializer(settings.SECRET_KEY)
        active_code = serializer.loads(code)
        confirm = active_code["confirm"]
        print(confirm)
        matchObj = re.match(r'^(.*)?(\d)$', confirm)
        user_id = matchObj.group(2)
        print("===== active ----")
        print(user_id)

        # redis中或取register激活码
        active_code = conn.hget('register', user_id)
        if active_code:
            user_profile = UserProfile.objects.get(id=user_id)
            user_profile.is_active = 1
            user_profile.save()
            username = user_profile.username
            return render(request, 'index.html', {'username': username})
        else:
            return render(request, 'login.html', {'msg': '激活链接已失效', 'user_id': user_id})


def find_page(request):
    if request.method == 'get':
        return render(request, 'forgetpwd.html')

# 找回密码页面
class ForgetPassword(View):
    def get(self, request):
        forgetForm = ForgetForm()
        return render(request, 'forgetpwd.html', {'forgetForm': forgetForm})

    def post(self, request):
        form = ForgetForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email', '')
            user_profile = UserProfile.objects.filter(username=email)
            print(user_profile)
            if user_profile is not None:
                return render(request, 'password_reset.html', {'findPasswordForm': FindPasswordForm, 'user_email': email})
            else:
                return render(request, 'forgetpwd.html', {'forgetForm': ForgetForm, 'msg': '该用户不存在，请核实后输入'})
        else:
            return render(request, 'forgetpwd.html', {'forgetForm': ForgetForm})


# 重置密码
class ResetPassword(View):
    def get(self, request):
        pass

    def post(self, request):
        form = FindPasswordForm(request.POST)
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        user_email = request.POST.get('user_email', '')
        if form.is_valid():
            if password != password2:
                return render(request, 'password_reset.html', {'msg': '两次输入密码不一致'})
            else:
                user = UserProfile.objects.get(username=user_email)
                if user is not None:
                    pwd = make_password(password)
                    user.password = pwd
                    user.save()
                    return render(request, 'change_success.html')
        else:
            return render(request, 'password_reset.html', {'findPasswordForm':FindPasswordForm})


# 重发激活邮件
def reActiveEmail(request):
    u_id = request.GET.get('id')
    print("----chong fa you jian---")
    print(u_id)
    user_profile = UserProfile.objects.get(id=u_id)
    to_email = user_profile.email
    send_type = 'register'
    status = send_asyn_active_email.delay(to_email, send_type, u_id)
    return JsonResponse({'status': status})



# def myMail(request):
#     if request.method == 'GET':
#         print("---发邮件ing---")
#         to_email = '417115351@qq.com'
#         username = 'test01'
#         send_register_active_email(to_email, username)
#         return HttpResponse('测试发邮件')
