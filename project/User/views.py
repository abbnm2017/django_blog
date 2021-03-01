# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from User.forms import UserRegisterForm, RegisterForm, LoginForm, PaChongForm
from User.models import UserProfile,MessageBoard,LikeCount, LikeRecord,ImgK,PcImgK,student,allclass,tea2class,teacher,testdata,testinfo,abbnm,Boy,Girl,Love
from django.db.models import Q  # 导入F类
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
# from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password, check_password
# from . import forms

# from User.utils import util_sendmsg
from .visit_info import change_info

from django.contrib import messages

from django.http import JsonResponse

from django.contrib.contenttypes.models import ContentType
# Create your views here.

from  django.core.exceptions import ObjectDoesNotExist

from django.views.decorators.cache import cache_page

from .pachongnew import Run

from django.views.decorators.csrf import csrf_exempt

from dwebsocket.decorators import accept_websocket

import utils.sqlhelper as sqlhelper

import utils.producename as producename

import simplejson as json

#RJ4587

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

def need4(request):
    return render(request, 'user/need4.html')

def need5(request):
    return render(request,'user/need5.html')

def need6(request):
    return render(request, 'user/need6.html')

def need7(request):
    return render(request,'user/need7.html')


def loading(request):
    return render(request,'user/fbv.html')

def floatpic(request):
    return render(request,'user/lunxun.html')

def tcp_socket(request):

    return render(request,'user/tcp_socket.html')

def nginx2(request):

    return render(request,'user/nginx.html')


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



def uploadImg(request):
    #图片上传
    if request.method == "POST":
        print("kekeke11111:%s"%request.FILES.get('img'))
        print("kekeke100022222:%s"%request.FILES.get('img').name)

        #
        # img_new_obj = request.FILES.get('img').replace()

        # python2.7
        # new_img = ImgK(
        #     img = request.FILES.get('img').replace(".MOV","mp4"),
        #     name = request.FILES.get('img').name.replace(".MOV","mp4"),
        #
        #     )
        #python3
        new_img = ImgK(
            img=request.FILES.get('img'),
            name=request.FILES.get('img').name.replace(".MOV", "mp4"),

        )

        new_img.save()

        messages.info(request,'上传成功')
        return redirect(reverse('User:showImg'))


    return render(request,'user/uploadpic.html')



def showImg(request):
    imgs = ImgK.objects.all()
    if len(imgs) > 0:
        print ("keke111:%s"%imgs)
        print ("keke222:%s"%imgs[0])
        print ("keke333:%s"%imgs[0].img)
        print ("keke444:%s"%imgs[0].name)

    new_video = []

    new_img = []

    for imgobj in  imgs :
        c_name = imgobj.name
        new_name = c_name.split('.')
        if new_name[-1] == "mp4" or new_name[-1] == "MOV":
            new_video.append(imgobj)
        else:
            new_img.append(imgobj)

    content = {
        'imgs':new_img,
        'videos':new_video,
    }
    # for i in imgs:
    #     print (i.img.url)
    return render(request,'user/showpic.html',content)



# def chat(request):
#
#     return render(request,'user/chat_index.html')

@cache_page(1*1)  #秒数 （一般是 60 * 15 ） 代表15分钟
def reptile(request):
    if request.method == "POST":
        lform = PaChongForm(request.POST)
        print ("pachong_1111:%s" % lform)
        print ("pachong_2222:%s" % lform.is_valid())
        if not lform.is_valid():
            messages.info(request, '图片名长度至少2位以上')

            return redirect(reverse('User:reptile'))
        playername = lform.cleaned_data.get('playername')
        page_num = lform.cleaned_data.get('page_num')
        # imporongnew
        Run(playername,page_num)



        imgs = PcImgK.objects.all()

        print ("keke_tttttoooo:%s"%imgs)
        #请求后的数据

        content = {
            'imgs': imgs,
        }

        #Ctrl + Alt + Space  快速导入任意类
        return render(request,'user/pachong.html',content)

    imgs = PcImgK.objects.all()
    content = {
        'imgs': imgs,
    }
    return render(request,'user/pachong.html',content)


person_list = []

# @csrf_exempt
def chatlogin(request):
    print("gggg----------p", person_list)
    request.session.flush()
    nickname = request.POST.get('nickname')


    if nickname in person_list:
        # person_list.append(nickname)
        request.session['msg'] = 'CurName had exist!'
        # request.session['nickname'] = nickname
        return redirect(reverse('User:chat'))
    if nickname != None:
        person_list.append(nickname)
        request.session['nickname'] = nickname

    return redirect(reverse('User:chat'))

def chat(request):
    print("我自己的呢-->",person_list )
    nickname = request.session.get('nickname')
    print("我自己的呢222-->", nickname)
    if nickname:
        return render(request,'user/chat.html',{'person_list':person_list})
    print("gggg6666", request.session.get('nickname'))
    return render(request,'user/chatlogin.html')

def chatlogout(request):

    nickname = request.GET.get('nickname')

    print ("keke_log--out",nickname)
    flag = 0
    for i in range(len(person_list)):
        if person_list[i] == nickname:
            print ('flag:', flag)
            flag = i
    if len(person_list) != 0:
        person_list.pop(flag)
    request.session.flush()

    print("keke_log--out", person_list)
    return redirect(reverse('User:chat'))

allconn = []

@accept_websocket
def conn(request):
    print ("kekemememe33333")
    global allconn
    if request.is_websocket():
        allconn.append(request.websocket)
        for message in request.websocket:
            for i in allconn:
                if i!=request.websocket:
                    i.send(message)


def classes(request):

    print ("keke_classes:%s"%request)
    print("keke_classes:%s" % request.method)

    #eg: sql="insert into cdinfo values(%s,%s,%s,%s,%s)"

    # sql = "select * from user_messageboard"

    sql = "select * from User_allclass"

    result = sqlhelper.get_list(sql,())


    print ("查看所有班级信息:",result)

    # print ("cur_state:%s"%result)

    # sql = """select * from User_teacher left join User_tea2class on User_teacher.id = User_tea2class"""


    return render(request,"user/class.html",{"message_result":result})

# csrf_exempt 不检测csrf   (setting.py 不注释)
# csrf_protect 检测csrf    (setting.py 注释)

# from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def addstudent(request):

    print ("###########",request)

    if request.method == "GET":
        now_time = sqlhelper.get_now_time()
        print ("kpl_cur_time:%s"%now_time)

        return render(request, "user/addstudent.html")


    else:

        name = request.POST.get("name1")
        content = request.POST.get("name2")

        sql = "select * from User_allclass"
        result = sqlhelper.get_list(sql, ())


        print ("1007777:%s"% request.POST.get("name1"))
        print("1007777:%s" % request.POST.get("name2"))

        # sql = "insert into User_messageboard(name,date,content) value (%s,%s,%s,%s)"
        # result = sqlhelper.modify(sql, (len(result) + 1, name, "2020.9.16",content))

        cur_data_time = sqlhelper.get_now_time()

        # sql = "insert into User_messageboard(name,date,content) values (%s,%s,%s)"
        # # args = [name, "2020.9.17", content]
        # args = [name, cur_data_time, content]
        # sqlhelper.modify(sql, args)

        sql = "insert into User_allclass(cls_title) values (%s)"
        args = [content]

        sqlhelper.modify(sql, args)

        return redirect(reverse('User:classes'))


def edit_student(request):
    if request.method == "GET":
        cur_id = request.GET.get("nid")
        print ("keke_cur_id:%s"%cur_id)
        #查询数据库

        sql = "select id,cls_title from User_allclass where id= %s"
        args = [cur_id]


        result_list = sqlhelper.get_one_list(sql,args)

        print ("keke:getsql",result_list)

        return render(request, 'user/editstudent.html',{"result_list":result_list})
    else:
        cur_id = request.GET.get("pid")
        name = request.POST.get("name1")
        content = request.POST.get("name2")

        print("keke_提交表单:%s" % cur_id)
        sql = "update User_allclass set cls_title = %s where id = %s"
        args = [content,cur_id]
        sqlhelper.modify(sql,args)
        return redirect(reverse('User:classes'))


def del_student(request):
    cur_id = request.GET.get("nid")
    print ("keke班级删除这个数据:%s"%cur_id)

    cur_id2 = request.POST.get("tgp")
    print ("keke:ajax:传过来的:%s"%cur_id2)


    sql = "delete from User_allclass where id = %s"
    args = [cur_id,]
    sqlhelper.modify(sql, args)
    # messages.info(request, '删除成功')
    return redirect(reverse('User:classes'))

#模态删除。。。。
def del_student2(request):
    cur_id = request.GET.get("nid")
    print ("keke删除这个数据:%s"%cur_id)

    cur_id2 = request.POST.get("tgp")
    print ("keke:ajax:传过来的:%s"%cur_id2)


    sql = "delete from User_allclass where id = %s"
    args = [cur_id2,]
    sqlhelper.modify(sql, args)
    # messages.info(request, '删除成功')
    return HttpResponse("ok")


def modal_addstudent(request):
    dy_sname = request.POST.get("title")
    dy_content = request.POST.get("title2")

    get_cur_title = request.POST.get("title")

    print ("keke添加学生弹出框:%s,%s"%(dy_sname,dy_content))

    # print("keke添加学生弹出框:%s" % (get_cur_title))

    if len(dy_content) > 0:
        # cur_data_time = sqlhelper.get_now_time()
        # sql = "insert into User_messageboard (name, date,content) values(%s,%s,%s)"
        # args = (dy_sname,cur_data_time,dy_content)
        sql = "insert into User_allclass(cls_title) values(%s)"
        args = [dy_content]
        sqlhelper.modify(sql,args)
        return HttpResponse("ok")
    else:
        return HttpResponse("班级标题不能为空")

    #如果是用post的表单 提交的话， 则可以 使用redirect

    #如果是ajax的话，只能是返回的字符串 只能是用js写

    # cur_data_time = sqlhelper.get_now_time()
    #
    # sql = "insert into User_messageboard (name, date,content) values(%s,%s,%s)"
    #
    # args = (dy_sname,cur_data_time,dy_content)
    #
    # sqlhelper.modify(sql,args)
    # import time
    # time.sleep(5)

    return HttpResponse("aopang")

    return redirect(reverse('User:classes'))

# 让网站好看起来，---------Bootstrap   fontawesome
#模态编辑框
def modal_addstudent2(request):
    # 一个对象转化成字符串   序列化
    # 字符串转化成对象      反序列化

    ret = {"status":True,"message":None}

    try:

        dy_sname = request.POST.get("name")
        dy_id = request.POST.get("cur_id")

        dy_content = request.POST.get("content")

        print ("keke编辑学生弹出框222:%s,%s"%(dy_id,dy_content))

        if  len(dy_content) > 0:
            cur_data_time = sqlhelper.get_now_time()
            # sql = "update User_messageboard set name= %s,content = %s  where id=%s"
            sql = "update User_allclass set cls_title = %s where id = %s"
            args = (dy_content,dy_id)
            sqlhelper.modify(sql,args)

    except Exception as e:
        ret['status'] = False
        ret['message'] = "处理异常"


    need_string = json.dumps(ret)

    print ("keke_json--dict to string:%s"%need_string)

    return HttpResponse(need_string)


def newstudent(request):
    sql = "select * from User_allclass"
    classes_list = sqlhelper.get_list(sql,[])
    # print("keke:%s"%classes_list)
    sql2 = "select User_student.id,User_student.name, User_allclass.cls_title,User_student.class_id from User_student left JOIN" \
           " User_allclass on User_student.class_id = User_allclass.id"

    student_list = sqlhelper.get_list(sql2,[])
    return render(request,'user/students.html',{"class_list":classes_list,"student_list":student_list})

def del_student_nowlist(request):
    ret = {"status": True, "message": None}
    student_id = request.POST.get('del_pid')
    class_id = request.POST.get("del_classid")
    print ("keke删除学生和班级对应关系:%s,%s"%(student_id,class_id))
    student_obj_list = student.objects.all()
    for stu_obj in student_obj_list:
        print ("kekedd--:",stu_obj.id, stu_obj.name,stu_obj.class_id)

    print ("keke:queryset_student:%s"%student_obj_list)

    student.objects.filter(id = student_id).delete()

    string_ret = json.dumps(ret)
    return HttpResponse(string_ret)

def edit_student_list(request):
    ret = {"status":True,"message":None}
    if request.method == "GET":
        print ("keke111222")
        student_id = request.GET.get("nid")

        sing_student_obj = student.objects.filter(id = student_id)
        print("keke1111,%s" % sing_student_obj[0].id)
        print("keke1111,%s" % sing_student_obj[0].name)
        sing_student_title =  sing_student_obj[0].class_id

        class_all_obj = allclass.objects.all()

        return render(request,'user/editstudent2.html',{"sing_student_id":sing_student_obj[0].id,"sing_student_name":sing_student_obj[0].name,
                                                        "class_list":class_all_obj,
                                                        "sing_student_title":sing_student_title,
                                                        })
    else:
        print("keke333444")
        pid2 = request.GET.get("pid")
        pname1 = request.POST.get("name1")
        pname2 = request.POST.get("name2")
        scroll_id = request.POST.get("classId")

        student_all_list = student.objects.all()
        student.objects.all().filter(id=pid2).update(name=pname2,class_id=scroll_id)
        print("keke333444:%s,%s,%s,%s"%(pid2,pname1,pname2,scroll_id))

        return redirect('/user/newstudent')

    string_ret = json.dumps(ret)
    return HttpResponse(string_ret)

def modal_add_student(request):
    ret = {"status":True,"message":None}
    name = request.POST.get("name")
    class_id = request.POST.get("class_id")
    print ("keke_模态添加学生:%s,%s"%(name,class_id))
    #序列化

    sql = "insert into User_student(name , class_id ) values (%s,%s)"
    args = [name,class_id]
    sqlhelper.modify(sql,args)

    string_ret = json.dumps(ret)
    return HttpResponse(string_ret)

def update_add_student(request):
    ret = {"status":True,"message":None}
    name = request.POST.get("name")
    class_id = request.POST.get("class_id")
    n_id = request.POST.get("nid")

    print ("keke_更新添加学生---:%s,%s,%s"%(name,class_id,n_id))
    #序列化

    sql = "update User_student set name = %s, class_id = %s where id = %s"

    args = [name,class_id,n_id]



    # sql = "insert into User_student(name , class_id ) values (%s,%s)"
    # args = [name,class_id]
    sqlhelper.modify(sql,args)

    string_ret = json.dumps(ret)
    return HttpResponse(string_ret)

def teachers(request):
    # teacher_list = sqlhelper.get_list("select id ,teacher_name from User_teacher",[])

    sql = "select User_teacher.id as tid ,User_teacher.teacher_name, User_allclass.cls_title from User_teacher \
        left join User_tea2class on User_teacher.id = User_tea2class.teacher_id  \
        left join User_allclass on User_tea2class.class_id = User_allclass.id\
        "
    result = sqlhelper.get_list(sql,[])
    # print ("dddbbb:%s"%result)
    # 处理数据
    result_dict = {}
    for item in result:
        if item["tid"] in result_dict:
            result_dict[item["tid"]]["titles"].append(item["cls_title"])
        else:
            result_dict[item["tid"]] = {"tid":item["tid"],"teacher_name":item["teacher_name"],"titles":[item["cls_title"]]}

    print ("111:",result_dict.values())

    teacher_list = result_dict.values()

    sql2 = "select * from User_allclass"
    class_list = sqlhelper.get_list(sql2,[])


    print ("老师表:%s"%teacher_list)
    return render(request,"user/teachers.html",{"teacher_list":teacher_list,"class_list":class_list})

def add_teachers(request):
    # print ("request.POST:%s",request.POST)
    # return HttpResponse("123466")
    ret = {"status":True,"message":None}
    name = request.POST.get("name")
    class_id = request.POST.getlist("class_ids[]")

    print ("科科添加老师:%s,%s"%(name,class_id))
    #老师表增加数据
    sql1 = "insert into User_teacher(teacher_name) value(%s)"
    args1 = [name]
    #老师和班级关系表中插入数据
    #获取当前添加的老师id=2
    #假设是2， 测试2,3
    #2,4
    #2,5
    # 一次连接，一次提交

    sqlobj = sqlhelper.SqlHelper()

    last_id = sqlobj.create(sql1,args1)
    print ("cur_obj:%s"%sqlobj)
    arg_list = []
    for cls_id in class_id:
        arg_list.append([last_id,cls_id])


    sql = "insert into User_tea2class(teacher_id,class_id) values(%s,%s)"
    args = arg_list
    sqlobj.multiple_modify(sql,args)
    sqlobj.close()

    return HttpResponse(json.dumps(ret))

    # teache_id = sqlhelper.create(sql1,args1)
    #
    # for cls_id in class_id:
    #     sqlhelper.modify("insert into User_tea2class(teacher_id,class_id) value(%s,%s)",[teache_id,cls_id])

def edit_teacher(request):
    if request.method == "GET":
        nid = request.GET.get("nid")
        obj = sqlhelper.SqlHelper()
        teacher_info = obj.get_one("select id, teacher_name from User_teacher where id=%s",[nid])
        class_id_list = obj.get_list("select class_id from User_tea2class where teacher_id = %s",[nid])
        class_list = obj.get_list("select id,cls_title from User_allclass",[])
        obj.close()
        # print ("keke:%s"%teacher_info)
        # print("keke00:%s" % class_id_list)

        temp = []
        for i in class_id_list:
            temp.append(i['class_id'])

        print ("keke7788:%s"%temp)

        print("keke22:%s" % class_list)
        # return HttpResponse("ok")
        return render(request,'user/edit_teacher.html',{
            'teacher_info':teacher_info,
            'class_id_list':temp,
            'class_list':class_list,
        })
    else:
         #url 传参自动放入get里面了
         nid = request.GET.get("nid")
         name = request.POST.get("name")
         class_ids = request.POST.getlist("class_ids")

         print ("keke33:%s,%s,%s"%(nid,name,class_ids))
         obj = sqlhelper.SqlHelper()
         # 更新老师表
         obj.modify("update User_teacher set teacher_name = %s where id=%s",[name,nid])
         # 更新老师和班级关系表
         #先把当前老师和班级关系 删除，然后在添加
         obj.modify("delete from User_tea2class where teacher_id = %s",[nid,])
         #
         data_list = []
         for cls_id in class_ids:
             temp = (nid,cls_id)
             data_list.append(temp)

         obj.multiple_modify("insert into User_tea2class(teacher_id,class_id) values(%s,%s)",data_list)
         obj.close()

         return redirect('/user/teachers')

def del_teacher_info(request):
    ret = {"status":True,"msg":None}
    teacher_id = request.POST.get("teacher_id")
    print ("889999:%s"%teacher_id)

    single_t2cobj = tea2class.objects.all().filter(teacher_id = teacher_id)

    single_teaobj = teacher.objects.all().filter(id = teacher_id)


    print("889999:%s" % single_t2cobj)
    single_t2cobj.delete()

    single_teaobj.delete()

    string_ret = json.dumps(ret)
    return HttpResponse(string_ret)

def newadd_teacher(request):
    import time
    time.sleep(1)
    obj = sqlhelper.SqlHelper()
    class_list = obj.get_list("select id ,cls_title from User_allclass",[])
    obj.close()
    print ("dddd:%s"%class_list)
    ret = json.dumps(class_list)
    print("ddddccc:%s" % ret)
    return HttpResponse(ret)


def layout(request):

    return render(request,'layout.html')

def test_fenye(request):
    print ("keke1222",producename)

    NameWidget_obj = producename.NameWidget()


    # print ("kekedd:%s"%all_random_name)

    all_random_name = ""

    # testdata.objects.create(**{"name":"二级用户"})

    # objs = [
    #     testdata(name="三级用户"),
    #     testdata(name="牛逼用户"),
    #     testdata(name="超级用户"),
    # ]
    #
    # testdata.objects.bulk_create(objs)


    # for _ in range(1,50+1):
    #     all_random_name = NameWidget_obj.RandomCreateName()
    #     all_password =NameWidget_obj.RandomCreatePwd()
    #     all_age = NameWidget_obj.RandomCreateAge()
    #     all_ug_id = NameWidget_obj.RandomCreateUg()
    #     testinfo.objects.create(user=all_random_name,password = all_password, age= all_age, ug_id = all_ug_id)

    # password = NameWidget_obj.RandomCreatePwd()
    # print("kekedd----:%s" % password)

    # testdata.objects.filter(id__gt=300).delete()
    test_list = testinfo.objects.all()

    # for cur_obj in test_list:
    #     want_id = cur_obj.testinfo_set.all()
    #     print ("kekebb900:%s"%want_id)
    v = test_list.values("nid",'user','ug','ug_id',"ug__name")

    # print ("keke1000:%s"%v)

    all_count = test_list.count()

    page_info = producename.PageInfo(1, all_count, "/user/custom",10)

    testname_list = testinfo.objects.all()[page_info.start():page_info.end()]

    print ("keke:ccc:%s"%testname_list[0].ug.name)
    # 如果这里是一个类对象
        #     cur_obj.ug.id
        #     cur_obj.ug.title
    # 如果这里是直接拿值  (要用双下划线)
        # testinfo.objects.values('nid','ug_id','ug__title')
        # testinfo.objects.values_list('nid','ug_id','ug__title')

    # 反向拿表(+set)
    #     如果这里是一个类对象
    #         new_obj = user_testdata.objects.all().first()
    #         result = new_obj.user_testinfo_set.all()  [user_testinfo对象,user_testinfo对象]
    #     如果这里是直接拿值  (要用双下划线)
    #         v = user_testdata.objects.values('id','name','user_testinfo__password')

    # v = testinfo.objects.values('ug_id')    #list - dict
    #
    # v2 = testinfo.objects.values_list('ug_id')  # list - tumper
    #
    # print ("keke---:%s"%v)
    # print("keke---111:%s" % v2)
    #  分组操作
    from django.db.models import Count,Sum,Max,Min
    # v3 = testinfo.objects.values('ug_id').annotate(xxxx= Count('nid'))
    # print ("kkkmmme---22:%s"%v3)
    # print("kkkmmme---33:%s" % v3.query)  #xxxx别名
    # v4 = testinfo.objects.values('ug_id').annotate(xxxx=Count('nid')).filter(xxxx__gt=22)
    # print ("keke----444:%s"%v4)
    #
    # v5 = testinfo.objects.filter(nid__lt=10).values("ug_id").annotate(xxxx=Count('nid')).filter(xxxx__gt=2)
    # print("keke----555:%s" % v5)

    #testinfo.objects.filter(nid__lt=10)   小于
                             # nid__lte  小于等于
                            # nid__gt 大于
                            # nid__gte 大于等于
    # testinfo.objects.filter(nid__in=[1,2,3])
    # testinfo.objects.filter(nid__range=[1,2])

    # v6 = testinfo.objects.filter(nid__range=[1,2])
    # print ("keke__ll:%s"%v6)
    # v7 = testinfo.objects.filter(user__startswith='贾螃蟹')
    # v8 = testinfo.objects.filter(user__contains='贾螃蟹')
    # v9 = testinfo.objects.exclude(nid=1)  #除nid=1以外的数据
    # print("keke__llv7:%s" % v7)

    # F，Q，extra
    # from django.db.models import F，Q
    # # F 是获取数据库里面的对象(原来的值)
    # testinfo.objects.all().update(age = F('age')+1)   #给全体数据都 + 1
    # con = Q()
    # q1 = Q()
    # q1.connector = 'AND'
    # q1.children.append(('id',1))
    # q1.children.append(('id',2))
    #
    # con.add(q1,'AND')
    # con.add(q2, 'AND')


    # testinfo.objects.extra(select=None, where=None, params=None, tables=None,
    #           order_by=None, select_params=None)

    # s = testinfo.objects.extra(
    #     select = {'new_id':'select count(1) from user_testinfo where nid > %s'},
    #     select_params = [95,],
    #     where = ['age > %s'],
    #     params = [18,],
    #     order_by = ['-age'],
    #     # tables = ['user_testdata']
    #     )
    #
    # print("keke扫描",s)

    # #原生SQl语句
    # from django.db import connection, connections
    #
    # cursor = connection.cursor()     #connection 是default数据库
    # print ("keke游标1：:%s"%cursor)
    # cursor = connections['default'].cursor()
    # ## cursor = connections['db2'].cursor()
    # print("keke游标2：:%s" % cursor)
    # # setting DATABASES 里面可以包括多种类型的数据库， 默认都用default(可选择链接哪个数据库)
    # cursor.execute("select count(1) from user_testinfo")
    #
    # row = cursor.fetchall()
    #
    # print ("keke游标3:",row)

    # result = testinfo.objects.filter(nid__gt=1).extra(
    #     where = ['user_testinfo.nid < %s'],
    #     params = [50],
    #     tables = ['user_testdata'],
    #     order_by = ['user_testinfo.nid'],
    #     select = {
    #         'uid':1,
    #         'sw':"select count(1) from user_testinfo",
    #     }
    # )
    # print ("keke--sql:%s"%result.query)
    # print("keke--sql22:%s" % result[0].sw)

    # 去重: select distinct age from user_testinfo;

    v91 = testinfo.objects.all()
    print ("keke_mmm:%s"%v91)


    v92 = testinfo.objects.values('nid','user')
    print ("keke_mmmv92:%s"%v92)

    v93 = testinfo.objects.all().only('nid','user')
    # v93 = testinfo.objects.all().defer('user') #除了user以外的
    print("keke_mmmv93:%s" % v93)

    # v94 = testinfo.objects.all().using('db2')   #指定去哪个数据库取数据
    # v94 = testinfo.objects.all().using('default')

    v95 = testinfo.objects.aggregate(k=Count('ug_id',distinct=True),n = Count('nid'))

    print ("keke_聚合:",v95)

    v96 = abbnm.objects.all()     #有了列才能创建
    # v97 = abbnm.objects.create(md=1)
    v97 = abbnm.objects.create(**{'md':6})
    print ("keke_测试数据",v97)

    #创建
    # testinfo.objects.create(title='xxx')
    # == testinfo.objects.create(**{'title':'xxx'})
    #
    # 或者:
    # obj = testinfo(title='xxx')
    # obj.save()
    # 两种创建方式

    print ("keke_aaaaaaaaaaa",Boy())
    #
    # #创建多对多
    # objs = [
    #     Boy(name='方少伟'),
    #     Boy(name='由清兵'),
    #     Boy(name='陈涛'),
    #     Boy(name='炎龙'),
    # ]
    #
    # Boy.objects.bulk_create(objs,5)
    #
    # objs = [
    #     Girl(nick='小鱼'),
    #     Girl(nick='小周'),
    #     Girl(nick='小苗'),
    #     Girl(nick='小狗'),
    # ]
    #
    # Girl.objects.bulk_create(objs, 5)

    # Love.objects.create(b_id=1,g_id=1)
    # Love.objects.create(b_id=1, g_id=4)
    # Love.objects.create(b_id=2, g_id=4)
    # Love.objects.create(b_id=2, g_id=2)
    # 1.查询和方少伟有关系的菇凉
    newobj= Boy.objects.filter(name="方少伟").first()

    print("查询和方少伟:",newobj,newobj.name, newobj.id, newobj.m)

    #如果是动态产生的第三方表 往第三方表插入数据
    # newobj.m.add(3)    # == boy_id= 1 girl_id=3
    # newobj.m.add(2,4)  # == boy_id= 1 girl_id=3 and boy_id=1 girl_id=4
    # newobj.m.add(*[1])

    # newobj.m.remove(1)
    #更新
    # newobj.m.set([3,])
    #获取
    # girl_list = newobj.m.all()
    # print ("abbnn111",girl_list[0].nick)

    obj = Boy.objects.filter(name='方少伟').first()
    # obj.m.clear()
    v= obj.m.add(1)
    print("keke_gggvvv", v)

    # obj = Girl.objects.filter(nick='小狗')
    # obj1 = Girl.objects.filter(nick='小狗').first()
    # print ("keke_ggg",obj)
    # print ("keke_ggg111", obj1)
    # v = obj1.boy_set.all()
    # print("keke_gggvvv", v)

    # 反向查找外键
    # a = newobj.love_set.all()
    # print ("n11111",a)
    # nick_list = []
    # for row in a:
    #     cur_nick = row.g.nick
    #     nick_list.append((cur_nick))
    # print("所有女孩子的名字",nick_list)
    #
    # dd = Love.objects.filter(b__name='方少伟')
    #
    # dd = Love.objects.filter(b__name='方少伟').values('g__nick')
    # print ("sss111:%s"%dd)
    # for hol in dd:
    #     print("sss111222:%s" % hol.g.nick)

    # dd = Love.objects.filter(b_name=1)
    #
    # print ("tttttttrr",dd)
    # 或者
    # dd = Love.objects.filter(b__name='方少伟').select_related('g')
    # for row in dd:
    #     dd = row.g.nick
    #
    #     print("sss111:%s" % dd)

    return render(request,'user/testfenye.html',{"test_list":testname_list,"page_info":page_info.pager()})

def custom(request):
    current_age = request.GET.get("page")
    test_list = testinfo.objects.all()

    all_count = test_list.count()
    page_info = producename.PageInfo(current_age,all_count,'/user/custom',10)

    print ("keke222----:%s,%s"%(page_info.start(),page_info.end()))


    # return HttpResponse("123")
    testname_list = testinfo.objects.all()[page_info.start():page_info.end()]

    return render(request,'user/testfenye.html',{"test_list":testname_list,"page_info":page_info.pager()})

def csrf(request):
    if request.method == "GET":
        print ("keke-csrf-get:",request.GET)
        from User import models
        import time
        cur_time = time.time()
        # models.UserInfo.objects.create(username="kekeonesss",email="448521@qq.com",c_time = "2014-08-07",color=1)

        return render(request,'user/csrf.html',{"name":"gaoda"})
    else:
        print("keke-csrf-post:", request.POST)
        d_name = request.POST.get("user")
        print("keke-csrf-post-d_name:", d_name)

        return redirect(reverse('User:csrf'))




