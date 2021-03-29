from django.shortcuts import render,HttpResponse

# Create your views here.

from .forms import UserLoginForm,UserRegisterForm

from django.contrib.auth import authenticate,login,logout

from django.shortcuts import redirect
from django.urls import reverse

from User import models
# 引入验证登录的装饰器

from django.contrib.auth.decorators import login_required

from django.db.models import Q

from django.views import View

import random

def user_login(request):
    if request.method == "POST":
        print ("keke_normal_login",request.POST)

        user_login_form = UserLoginForm(data=request.POST)

        if user_login_form.is_valid():
            data = user_login_form.cleaned_data

            print ("kekell",data)

            # user = authenticate(username=data['username'], password=data['password'])

            user = models.UserProfile.objects.filter(username=data['username'],password=data['password']).first()

            print ("ddddd:%s"%user)

            print("kekell_cc", user)
            if user:
                login(request, user)

                return redirect(reverse('app01:article'))

            else:
                return HttpResponse('账号或密码输入有误。请重新输入~')

        return HttpResponse("ppp")

    else:
        user_login_form = UserLoginForm()

        context = {'form':user_login_form}

        return render(request,'normal/login.html',context)

        return HttpResponse('ok11')


def user_loginout(request):
    logout(request)
    return redirect('app01:article')

def create_phone():
    # 第二位数
    second = [3,4,5,7,8][random.randint(0,4)]
    # 第三位数
    third ={
        3:random.randint(0,9),
        4:random.randint(5,7),
        5:[i for i in range(0,10) if i != 4][random.randint(0,8)],
        7:random.randint(6,8),
        8:random.randint(0,9),
    }[second]
    # 后八位数
    suffix = ''
    for j in range(0,8):
        suffix = suffix + str(random.randint(0,9))

    return "1{}{}{}".format(second,third,suffix)


def user_register(request):
    if request.method == "POST":
        print ("keke_method",request.POST)
        user_register_form = UserRegisterForm(request.POST)

        if user_register_form.is_valid():
            print ("33333333333")
            username = user_register_form.cleaned_data["username"]
            email= user_register_form.cleaned_data["email"]
            password = user_register_form.cleaned_data["password"]
            user = models.UserProfile.objects.create(username=username, password=password, email=email,mobile=create_phone())

            if user:
                login(request,user)
                return redirect('app01:article')

        else:
            print ("kekeggg",user_register_form.errors)

        txt = ""
        if  user_register_form.errors.get("username"):
            txt += user_register_form.errors["username"][0]
        if user_register_form.errors.get("password"):
            txt += user_register_form.errors["password"][0]
        if user_register_form.errors.get("email"):
            txt += user_register_form.errors["email"][0]
        return HttpResponse(txt)

    else:
        return render(request,'normal/register.html')


@login_required(login_url='/normal/login/')
def user_delete(request,user_id):

    print ("7778899keke",user_id,request.user)

    if request.method == 'POST':
        user = models.UserProfile.objects.filter(id = user_id).first()

        print ("new555,",user)


        if request.user == user:
            logout(request)
            user.delete()
            return redirect('app01:article')
        else:
            return HttpResponse("你没有删除操作的权限")
    else:
        return HttpResponse("我传错了吗？？")


#pip install -U django-password-reset

#pip install django-taggit

#pip install django-ckeditor

#pip install django-notifications-hp

#pip install django-mptt


#https://www.dusaiphoto.com/article/46/



