
from django.shortcuts import render,HttpResponse,redirect
from User import models
from django.urls import reverse
def login(request):
    if request.method == 'GET':
        print ("kekeazzzz:11111")
        return render(request,'marry/marrylogin.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        gender = request.POST.get('gender')
        rmd = request.POST.get('rmb')
        print ("keke-结婚数据:%s,%s,%s,%s"%(user,pwd,gender,rmd))

        #性别判断
        if gender == "1":
            obj = models.MarryBoy.objects.filter(username=user,password=pwd).first()
        else:
            obj = models.MarryGirl.objects.filter(username=user,password=pwd).first()

        if not obj:
            #未登录
            return render(request,'marry/marrylogin.html',{'msg':'用户名或密码错误'})
        else:
            # request.session['user_id'] = obj.id
            # request.session['gender'] = gender
            # request.session['username'] = user
            print ("dddddddddd,",obj.id,obj.nickname)
            request.session['user_info'] = {'user_id':obj.id,'gender':gender,'username':user,'nickname':obj.nickname}
            return redirect(reverse('User:love_index'))


def logout(request):
    # request.session.delete(request.session.session_key) #删除表里的数据
    request.session.clear() #删除cookies
    return render(request,'marry/marrylogin.html')


def judge_handle_decorate(fun):

    def walkhande(*args,**kwargs):
        print ("keke--开始执行装饰器")
        # print ("keke:dddd-----",(*args, *kwargs))

        # return HttpResponse('404')

        ret = fun(*args,**kwargs)

        print("keke---结束执行装饰器")
        return ret
    return walkhande


@judge_handle_decorate
def test(request):
    boy = models.MarryBoth.objects.filter(gender=1,id=2).first()

    girl = models.MarryBoth.objects.filter(gender=2,id=6).first()
    # print("keke00000000000:",boy.nickname)
    #
    # print("keke000000000001:", girl.nickname)

    # print ("keke1111:%s"%boy.b_id)
    # print ("keke333:%s" %boy.g_id)
    # models.U2U.objects.create(b_id=boy.id,g_id=girl.id)
    #第一种
    # models.U2U.objects.create(b_id=1,g_id=6);
    # models.U2U.objects.create(b_id=1,g_id=4);
    # models.U2U.objects.create(b_id=1,g_id=5);
    #第二种
    # models.U2U.objects.create(b=boy,g = girl)
    # obj_p = models.U2U.objects.filter(b_id = 1)

    hg = models.MarryBoth.objects.filter(id=1).first()

    # #第一种
    # print("kekecc_男:%s" % hg.boys.all())
    # print ("kekecc_女:%s"%hg.girls.all())
    # #第二种
    # # print("kekecc_男:%s" % hg.U2U_set.all())
    #
    # for obj in hg.girls.all():
    #     print("kekecc_单个:%s" % obj.g.nickname)

    comment_obj = models.Comment.objects.all()

    comment_obj = models.Comment.objects.filter(news_id = 1)

    # print("当前评论", comment_obj)
    # exist_list = []
    # for i in comment_obj:
    #     if i.reply :
    #         exist_list.append(i)
    # print ("存在",exist_list)
    #
    # first_obj = exist_list[0].reply_id.all()
    #
    # print ("kekedi one",first_obj)

    print ("执行视图函数account_test")


    return HttpResponse("ok")



