# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from User.forms import UserRegisterForm, RegisterForm, LoginForm, PaChongForm
from User.models import UserProfile,MessageBoard,LikeCount, LikeRecord,ImgK,PcImgK
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
    return render(request,'user/loading.html')

def floatpic(request):
    return render(request,'user/floatpic.html')


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

@csrf_exempt
def chatlogin(request):
    request.session.flush()
    nickname = request.POST.get('nickname')

    if nickname in person_list:
        person_list.append(nickname)
        request.session['msg'] = 'CurName had exist!'
        return redirect(reverse('User:chat'))
    if nickname != None:
        person_list.append(nickname)
        request.session['nickname'] = nickname

    return redirect(reverse('User:chat'))

def chat(request):
    nickname = request.session.get('nickname')
    if nickname:
        return render(request,'user/chat.html',{'person_list':person_list})
    return render(request,'user/chatlogin.html')

def logout(request):
    nickname = request.GET.get('nickname')
    flag = 0
    for i in range(len(person_list)):
        if person_list[i] == nickname:
            print ('flag:', flag)
            flag = i
    person_list.pop(flag)
    request.session.flush()
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

    sql = "select * from user_allclass"

    result = sqlhelper.get_list(sql,())


    print ("1111:",result)

    # print ("cur_state:%s"%result)

    # sql = """select * from user_teacher left join user_tea2class on user_teacher.id = user_tea2class"""


    return render(request,"user/class.html",{"message_result":result})


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

        sql = "insert into user_allclass(cls_title) values (%s)"
        args = [content]

        sqlhelper.modify(sql, args)

        return redirect(reverse('User:classes'))


def edit_student(request):
    if request.method == "GET":
        cur_id = request.GET.get("nid")
        print ("keke_cur_id:%s"%cur_id)
        #查询数据库

        sql = "select id,name, content from User_messageboard where id= %s"
        args = [cur_id]

        result_list = sqlhelper.get_one_list(sql,args)

        print ("keke:getsql",result_list)

        return render(request, 'user/editstudent.html',{"result_list":result_list})
    else:
        cur_id = request.GET.get("pid")
        name = request.POST.get("name1")
        content = request.POST.get("name2")

        print("keke_提交表单:%s" % cur_id)
        sql = "update User_messageboard set name = %s,content = %s where id = %s"
        args = [name,content,cur_id]
        sqlhelper.modify(sql,args)
        return redirect(reverse('User:classes'))


def del_student(request):
    cur_id = request.GET.get("nid")
    print ("keke删除这个数据:%s"%cur_id)

    cur_id2 = request.POST.get("tgp")
    print ("keke:ajax:传过来的:%s"%cur_id2)


    sql = "delete from User_messageboard where id = %s"
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


    sql = "delete from User_messageboard where id = %s"
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

    if len(dy_sname) > 0 and len(dy_content) > 0:
        # cur_data_time = sqlhelper.get_now_time()
        # sql = "insert into User_messageboard (name, date,content) values(%s,%s,%s)"
        # args = (dy_sname,cur_data_time,dy_content)
        sql = "insert into user_allclass(cls_title) values(%s)"
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

        print ("keke添加学生弹出框222:%s,%s"%(dy_sname,dy_content))

        if len(dy_sname) > 0 and len(dy_content) > 0:
            cur_data_time = sqlhelper.get_now_time()
            sql = "update User_messageboard set name= %s,content = %s  where id=%s"
            args = (dy_sname,dy_content,dy_id)
            sqlhelper.modify(sql,args)

    except Exception as e:
        ret['status'] = False
        ret['message'] = "处理异常"


    need_string = json.dumps(ret)

    print ("keke_json--dict to string:%s"%need_string)

    return HttpResponse(need_string)


def newstudent(request):
    sql = "select * from user_allclass"
    classes_list = sqlhelper.get_list(sql,[])
    # print("keke:%s"%classes_list)
    sql2 = "select user_student.id,user_student.name, user_allclass.cls_title,user_student.class_id from user_student left JOIN" \
           " user_allclass on user_student.class_id = user_allclass.id"

    student_list = sqlhelper.get_list(sql2,[])
    return render(request,'user/students.html',{"class_list":classes_list,"student_list":student_list})

def modal_add_student(request):
    ret = {"status":True,"message":None}
    name = request.POST.get("name")
    class_id = request.POST.get("class_id")
    print ("keke_模态添加学生:%s,%s"%(name,class_id))
    #序列化

    sql = "insert into user_student(name , class_id ) values (%s,%s)"
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

    sql = "update user_student set name = %s, class_id = %s where id = %s"

    args = [name,class_id,n_id]



    # sql = "insert into user_student(name , class_id ) values (%s,%s)"
    # args = [name,class_id]
    sqlhelper.modify(sql,args)

    string_ret = json.dumps(ret)
    return HttpResponse(string_ret)

def teachers(request):
    # teacher_list = sqlhelper.get_list("select id ,teacher_name from user_teacher",[])

    sql = "select user_teacher.id as tid ,user_teacher.teacher_name, user_allclass.cls_title from user_teacher \
        left join user_tea2class on user_teacher.id = user_tea2class.teacher_id  \
        left join user_allclass on user_tea2class.class_id = user_allclass.id\
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

    sql2 = "select * from user_allclass"
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
    sql1 = "insert into user_teacher(teacher_name) value(%s)"
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


    sql = "insert into user_tea2class(teacher_id,class_id) values(%s,%s)"
    args = arg_list
    sqlobj.multiple_modify(sql,args)
    sqlobj.close()

    return HttpResponse(json.dumps(ret))

    # teache_id = sqlhelper.create(sql1,args1)
    #
    # for cls_id in class_id:
    #     sqlhelper.modify("insert into user_tea2class(teacher_id,class_id) value(%s,%s)",[teache_id,cls_id])

def edit_teacher(request):
    if request.method == "GET":
        nid = request.GET.get("nid")
        obj = sqlhelper.SqlHelper()
        teacher_info = obj.get_one("select id, teacher_name from user_teacher where id=%s",[nid])
        class_id_list = obj.get_list("select class_id from user_tea2class where teacher_id = %s",[nid])
        class_list = obj.get_list("select id,cls_title from user_allclass",[])
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
         obj.modify("update user_teacher set teacher_name = %s where id=%s",[name,nid])
         # 更新老师和班级关系表
         #先把当前老师和班级关系 删除，然后在添加
         obj.modify("delete from user_tea2class where teacher_id = %s",[nid,])
         #
         data_list = []
         for cls_id in class_ids:
             temp = (nid,cls_id)
             data_list.append(temp)

         obj.multiple_modify("insert into user_tea2class(teacher_id,class_id) values(%s,%s)",data_list)
         obj.close()

         return redirect('/user/teachers')


def newadd_teacher(request):
    import time
    time.sleep(1)
    obj = sqlhelper.SqlHelper()
    class_list = obj.get_list("select id ,cls_title from user_allclass",[])
    obj.close()
    print ("dddd:%s"%class_list)
    ret = json.dumps(class_list)
    print("ddddccc:%s" % ret)
    return HttpResponse(ret)


def layout(request):

    return render(request,'layout.html')



