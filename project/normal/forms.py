# 引入表单类
from django import forms
# 引入 User 模型
# from django.contrib.auth.models import User
from User.models import UserProfile

from User.models import UserProfile



# 登录表单，继承了 forms.Form 类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

# 注册用户表单
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = UserProfile
        fields = ('username','email')


    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get("password2"):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致,请重试。")






