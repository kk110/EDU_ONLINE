from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserProfile(AbstractUser):
    birthday = models.DateField(null=True,blank=True,verbose_name='生日')
    nick_name = models.CharField(max_length=50, verbose_name='昵称')
    gender = models.CharField(max_length=10, choices=(('male', '男'), ('female', '女')),default='female')
    address = models.CharField(max_length=100,default='')
    mobile = models.CharField(max_length=11, blank=True, null=True)
    image = models.ImageField(max_length=100, upload_to='image/%Y%m', default="image/default.png")

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        db_table = 'UserProfile'

    def __unicode__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=200,verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(choices=(('register','注册'),('forget','找回')),max_length=10,verbose_name='验证码类型')
    send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')
    which_user = models.CharField(max_length=50, verbose_name='用户id')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name
        db_table = 'EmailVerifyRecord'

    def __unicode__(self):
        return '{0}{1}'.format(self.code, self.email)



class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name='标题')
    image = models.ImageField(upload_to='banner/%Y/%m',verbose_name='轮播图',max_length=100)
    url = models.URLField(max_length=200, verbose_name='访问地址')
    index  = models.IntegerField(default=100, verbose_name='图片顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
        db_table = 'Banner'


