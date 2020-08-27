# -*- coding: utf-8 -*-
import re
from django.core.exceptions import ValidationError
from django.forms import Form, ModelForm
from django import forms
from User.models import UserProfile



class UserRegisterForm(Form):
    username = forms.CharField(max_length=50, min_length=6, error_messages={'min_length':'用户名长度至少6位',},label="用户名")
    email = forms.EmailField(required=True, error_messages={'required':'必须填写邮箱信息'},label='邮箱')
    mobile = forms.CharField(required=True, error_messages={'required':'必须填写手机号码'},label='手机')
    password= forms.CharField(required=True,  error_messages={'required':'必须填写密码'},label='密码',widget=forms.widgets.PasswordInput)
    repassword = forms.CharField(required=True, error_messages={'required': '必须填写确认密码'}, label='密码',widget=forms.widgets.PasswordInput)
    # favorite_colors = forms.MultipleChoiceField(
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=(('blue','Blue'),('red','Red'),('green','Green'),('yellow','Yellow')), label = '最喜欢的颜色',
    # )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        result = re.match(r'[a-zA-Z]\w{5,}', username)
        if not result:
            raise ValidationError('用户名必须以数字开头')
        return username


class RegisterForm(ModelForm):
    repassword = forms.CharField(required=True, error_messages={'required': '必须填写确认密码'}, label='确认密码',
                                 widget=forms.widgets.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'mobile', 'password']
        # fields = '__all__'
        # exclude = ['first_name','date_joined','last_name']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # result = re.match(r'[a-zA-Z]\w{5,}', username)
        # if not result:
        #     raise ValidationError('用户名必须以数字开头')
        return username


class LoginForm(Form):
    username = forms.CharField(max_length=50, min_length=4, error_messages={'min_length': '用户名长度至少6位', }, label="用户名")
    password = forms.CharField(required=True, error_messages={'required': '必须填写密码'}, label='密码',
                               widget=forms.widgets.PasswordInput)



    # class Meta:
    #     model = UserProfile
    #     fields = ['username', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not UserProfile.objects.filter(username=username).exists():
            raise ValidationError('用户名不存在')
        return username


class PaChongForm(Form):
    playername = forms.CharField(max_length=50, min_length=2, error_messages={'min_length': '用户名长度至少6位', }, label="图片名")
    page_num = forms.CharField(max_length=2, min_length=1, error_messages={'min_length':'用户名长度至少6位',},label="页数")


