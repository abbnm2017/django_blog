# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from User.forms import UserRegisterForm, RegisterForm, LoginForm
from User.models import UserProfile,MessageBoard,LikeCount, LikeRecord
from django.db.models import Q  # 导入F类
from django.http import HttpResponse
from django.shortcuts import render, redirect
# from django.urls import reverse
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password, check_password
# from . import forms

from User.utils import util_sendmsg
from .visit_info import change_info

from django.contrib import messages

from django.http import JsonResponse

from django.contrib.contenttypes.models import ContentType
# Create your views here.

from  django.core.exceptions import ObjectDoesNotExist


def index(request):
    temp_count, total_count = change_info(request)
    return render(request, 'index.html', context={'msg1':'今日访问量：%s'%temp_count,'msg2':'历史访问量：%s'%total_count})


def user_register(request):
    if request.method == 'GET':
        print ("4445555")
        return render(request, 'user/register2.html')
    else:
        print ("keke12:",request.POST)
        rform = RegisterForm(request.POST)      #使用form获取数据

        print ("123:",rform.is_bound,rform.is_valid(),rform._errors)

        # username = rform.cleaned_data.get('username')
        # email = rform.cleaned_data.get('email')
        # mobile = rform.cleaned_data.get('mobile')
        # password = rform.cleaned_data.get('password')
        # print ("11:",username)
        # print ("22:",email)
        if rform.is_valid():#进行数据校验
            #从干净的数据中取值
            username = rform.cleaned_data.get('username')
            email = rform.cleaned_data.get('email')
            mobile = rform.cleaned_data.get('mobile')
            password = rform.cleaned_data.get('password')

            if not UserProfile.objects.filter(Q(username=username)|Q(mobile=mobile)).exists():
                # 注册到数据库中
                # password = make_password(password)     #密码加密
                user = UserProfile.objects.create(username=username,password=password,email=email,mobile=mobile)
                if user:
                    # return HttpResponse('注册成功')
                    messages.info(request,'注册成功')
                    return render(request, 'user/login.html')
            else:
                return render(request,'user/register2.html',context={'msg':'用户名或者手机号码已经存在'})
        return render(request,'user/register2.html',context={'msg':'注册失败,重新填写!'})



def user_login(request):
    if request.method == 'GET':

        return render(request, 'user/login.html')
    else:
        lform = LoginForm(request.POST)
        print ("1111:%s"%lform)
        print ("2222:%s"%lform.is_valid())
        if lform.is_valid():
            username = lform.cleaned_data.get('username')
            password = lform.cleaned_data.get('password')
            #进行数据库的查询
            user = UserProfile.objects.filter(username=username).first()

            flag = check_password(password, user.password)
            print ("haha111:%s" % flag)
            if flag:
                print ("haha:%s"%flag)

            print ("55:%s"%password)
            print("566:%s"%user.password)
            # check_password()
            if password == user.password:
                request.session['username'] = username
                # return HttpResponse('用户登录成功')
                return redirect(reverse('User:index'))         #appname +
        print("mmm:%s"%lform.errors)
        return render(request, 'user/login.html', context={'errors':lform.errors})


def user_logout(request):
    # request.session.clear()     #删除字典
    request.session.flush()     #删除django_session + cookie + 字典
    return redirect(reverse('User:index'))


def user_zhuce(request):
    if request.method == 'GET':
         rform = RegisterForm()
         # rform = forms.UserRegisterForm()

         print("111====>",rform)
         return render(request, 'user/zhuce.html', context = {'rform': rform})

    else:
        rform = UserRegisterForm(request.POST)
        # rform = forms.UserRegisterForm(request.POST)
        # print("222-->",rform)
        print("33",rform.is_valid())
        if rform.is_valid():
            print(rform.cleaned_data)
            username = rform.cleaned_data.get('username')
            email = rform.cleaned_data.get('email')
            mobile = rform.cleaned_data.get('mobile')
            password = rform.cleaned_data.get('password')


            #数据库中注册

        return HttpResponse('hah')


def failed(request):
    return HttpResponse("注册你马哥B")


def code_login(request):
    if request.method == 'GET':
        print("keke1111111111")
        return render(request, 'user/abbnm.html')
    else:
        mobile = request.POST.get('mobile')
        code = request.POST.get('code')

        #根据mobile去session中取值
        check_code = request.session.get(mobile)
        if code == check_code:
            return redirect(reverse('User:index'))
        else:
            return render(request, 'user/codelogin.html', context = {'msg':'验证码有误!'})


def about(request):
    return render(request, 'user/about.html')


def board(request):
    message_b = MessageBoard.objects.all()

    return render(request, 'user/leavemessage.html',{'le_messages':message_b})



def board_post(request):
    if request.method == 'POST':
        name = request.POST['name']
        content = request.POST['content']


        print ("keke__board_post:%s"%name)
        print ("keke__board_post222:%s" % content)

        uobj = MessageBoard.objects.all()
        print("keke_board_post333:%s"%uobj)
        # uobj.save()

        msg = MessageBoard.objects.create(name = name, content=content)


        messages.info(request,'留言成功')

        return redirect(reverse('User:board'))
    else:
        return HttpResponse("留言板请求方式GET，ERROR 状态，请返回首页")



def life_open(request):


    return render(request, 'user/lifeopen.html')


def zanshang(request):

    return render(request, 'user/zanshang.html')







#发送验证码 由ajax发过来的请求
def send_code(request):
    mobile = request.GET.get('mobile')
    #发送验证码 第三方

    json_result = util_sendmsg(mobile)
    # 取值:
    status = json_result.get('code')
    data = {}
    if status == 200:
        check_code = json_result.get('obj')

        #使用session保存
        request.session[mobile] = check_code

        data['status'] = 200
        data['msg'] = '验证码发送成功'
    else:

        data['status'] = 500
        data['msg'] = '验证码发送失败'

    return JsonResponse(data)

#手机验证码登录


def need1(request):
    print("keke_user_pk:%s"%request.user)
    print("keke_user_pk111:%s"%request.user.pk)
    return render(request, 'user/need1.html')


def need2(request):
    return render(request, 'user/need2.html')

def need3(request):
    return render(request,'user/need3.html')


#点赞
def test_ajax(request):
    name_dict = {'News':'Learning Ajax'}
    return JsonResponse(name_dict)



def ErrorResponse(code,message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def SuccessResponse(liked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)



def like_change(request):
    user = request.user

    cur_login_name = request.session.get('username')
    print ("keke:%s"%cur_login_name)
    if not cur_login_name:
        return ErrorResponse(400,'你没有登录')


    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))


    print ("keke_like_change:%s,%s"%(content_type,object_id))

    # try:

    ContentType.objects.all()
    for obj in ContentType.objects.all():
        print ("cnmm:%s"%obj)
    # print ("keke6666666667:%s"%ContentType.objects.all())
    # content_type = ContentType.objects.get(model=content_type)

    # model_class = content_type.model_class()
    # model_obj = model_class.objects.get(pk=object_id)

    print ("keke_zero1:%s"%ContentType.objects)
    # print ("keke_zero2:%s"%model_class)
    # print ("keke_zero3:%s"%model_obj)

    # except ObjectDoesNotExist:

        # return ErrorResponse(400,'对象不存在')

    


    is_like = request.GET.get('is_like')

    print ("keke_is_lock:%s"%is_like)

    #处理数据
    if is_like == 'true':
        #要点赞
        print ("keke:tttttttttttttttttttttt")
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type,object_id=object_id)
        
        if created:
            #未点赞过，进行点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        else:
            #已点赞过，不能重复点赞
            return ErrorResponse(402,'你已经点赞过')


    else:
        #要取消点赞
        print ("keke:ffffffffffffffffffffff")
        if LikeRecord.objects.filter(content_type=content_type,object_id=object_id,user=user).exists():
            #有点赞过取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type,object_id=object_id,user=user)
            like_record.delete()
            #点赞总数 -1 

            like_count, created = LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
            if not created:
                like_count.like_num -= 1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:
                return ErrorResponse(404,'数据错误')


        else:
            #没有点赞过，不能重复点赞
            return ErrorResponse(403,'你没有点赞过')











