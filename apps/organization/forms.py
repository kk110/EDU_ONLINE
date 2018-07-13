# _*_ coding: utf-8 _*_
__author__ = 'amy'
__date__ = '18-7-13 上午9:42'
import re

from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        """
        mobile = self.cleaned_data['mobile']
        regex_mobile = r'1[358]\d{9}$|^147\d{8}$|176\d{8}$'
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            return forms.ValidationError('手机号码非法', code='mobile_invalide')