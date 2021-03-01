from django.shortcuts import render,HttpResponse,redirect
import json
# Create your views here.

"""
Django Form 组件
    1.定义规则
"""
from django.forms import Form
from django.forms import fields
from django.forms import  widgets

from app01 import models

from .forms import ArticlePostForm

from User.models import UserProfile

from django.shortcuts import render, redirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.db.models import Q

from comment.models import Comment

from django.views import View

from .models import ArticleColumn

from comment.forms import CommentForm


class LoginForm(Form):
    #长度是否为空的的校验（正则的验证）
    username = fields.CharField(max_length=18,
                                min_length=6,
                                required=True,
                                error_messages={
                                    "min_length":"最短长度不得少于6位",
                                    "max_length": "最大长度不得超过18位",
                                    "required": "用户名不能为空",
                                },
                                )
    password = fields.CharField(min_length=16,required=True)

    t2 = fields.IntegerField(
        min_value=10,
        max_value =1000,
        required=True,
    )
    #代码生成 带有 规则的html
    t3 = fields.CharField(
        required=True,
        widget=widgets.Select,
        label="用户名 ",
        disabled=False,
        label_suffix="--->",
        initial="666",
        help_text="....help",
    )


class RegiterForm(Form):
    user = fields.CharField(
        min_length=8,
    )
    email = fields.EmailField()
    password = fields.CharField()
    phone = fields.RegexField('136\d+')


def login(request):

    if request.method == "GET":
        print ("222222222222222")
        return render(request,'app01/login.html')
    else:
        """

        user = request.POST.get("username")
        pwd = request.POST.get("password")
        print ("keke_app01---:%s,%s"%(user,pwd))
        # dict_desc = {
        #     "username":user,
        #     "password":pwd,
        # }
        # ret = json.dumps(dict_desc)
        if user == 'root' and pwd =='123':
            return redirect('http://www.baidu.com')
        else:
            return render(request,'app01/login.html',{"msg":"用户名或密码错误"})
        """

        obj = LoginForm(request.POST)
        ret = obj.is_valid()
        print ("打印djangoForm组件所有数据",obj.cleaned_data)
        print ("校验:",ret)
        if ret:   #提交成功
            pass
        else:
            print ("keke--失败",obj.errors)
            # print("keke--用户失败", obj.errors["username"][0])
            # print("keke--密码失败", obj.errors["password"][0])

            """
            html标签name属性 == Form类字段名
            #所有错误信息
            obj.errors

            #所有正确信息
            obj.cleaned_data


            http请求的生命周期 ---------> 请求->wsgi->中间件(process_request,process_response)-> 路由系统->视图函数（数据库处理数据）->返回给中间件-> 返回给wsgi->
                ->交给用户
                本质传递的是字符串

                session 是保存在服务器端的键值对(数据)

                cookies 是保存在客户端的键值对（数据）

                session的本质 是

                当用户来登录的时候，服务器生产随机字符串给浏览器，浏览器写到cookies里面了，
                服务器将这个随机字符串保存起来了，这个随机字符串可以对应一些值，这个值属于这个用户，每个用户就是一个随机字符串

                csrf-POST
                 跨站请求伪造 -----
                     银行
                     打开银行网站，打开自己（黑课）网站（像招商银行发POST请求，携带cookies 给我转账了）
                     防止这个，csrf发一个随机字符串，
                     不仅发送数据，还要发送随机字符串
                     随机字符串一定是上一次请求获取到的


                xss  用户提交 ，以安全的形式让用户看，当做字符串 评论（alert）
                     |safe 以安全方式
                     过滤关键字

            """
            return render(request,"app01/login.html",{"obj":obj})


def ajax_commit(request):
    ret = {"status":True,"msg":None}
    obj = LoginForm(request.POST)
    if obj.is_valid():
        print (obj.cleaned_data)
    else:
        print (obj.errors)
        v = json.dumps(obj.errors)
        print (v)
        ret['status'] = False
        ret['msg'] = obj.errors
    v = json.dumps(ret)
    return HttpResponse(v)

def mm_login(request):
    print ("123444444")
    if request.method == "GET":
        # return HttpResponse('ok')
        obj = RegiterForm()
        return render(request,"app01/moming_login.html",{'obj':obj})
    else:
        obj = RegiterForm(request.POST)
        if obj.is_valid():
            print (obj.cleaned_data)
        else:
            print (obj.errors)
        return render(request,'app01/moming_login.html',{'obj':obj})

def class_list(request):
    cls_list = models.Classes.objects.all()
    return render(request,'app01/class_list.html',{'cls_list':cls_list})

class ClassForm(Form):
    # title = fields.CharField()
    title = fields.RegexField('全栈\d+')

def add_class(request):
    if request.method == "GET":
        obj = ClassForm()
        return render(request,'app01/add_class.html',{'obj':obj})
    else:
        obj = ClassForm(request.POST)
        if obj.is_valid():
            print ("keke_添加班级:",obj.cleaned_data)
            #在数据库插入一条数据
            models.Classes.objects.create(**obj.cleaned_data)
            return redirect('/app01/class_list/')
        else:
            print ("keke_添加班级错误",obj.errors)
        return render(request, 'app01/add_class.html', {'obj': obj})

def edit_class(request,nid):
    if request.method == "GET":
        row = models.Classes.objects.filter(id=nid).first()
        #让页面显示初始值
        obj = ClassForm(initial={'title':row.title})   #默认并且不校验
        # obj = ClassForm(data={'title':row.title})  #默认并且校验
        return render(request,'app01/edit_class.html',{"row":row,'nid':nid,"obj":obj})
    else:
        obj = ClassForm(request.POST)
        if obj.is_valid():
            models.Classes.objects.filter(id=nid).update(**obj.cleaned_data)
            return redirect('/app01/class_list/')
        return render(request,'app01/edit_class.html',{'nid':nid,"obj":obj})

def student_list(request):
    stu_list = models.Student.objects.all()
    return render(request,'app01/student_list.html',{'stu_list':stu_list})

class StudentForm(Form):
    name = fields.CharField(
        min_length=2,
        max_length=6,
        widget = widgets.TextInput(attrs={'class':'form-control'}),
    )
    email = fields.EmailField(
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
    )
    age = fields.IntegerField(min_value=18,max_value=25,widget = widgets.TextInput(attrs={'class':'form-control'}),)
    cls_id = fields.IntegerField(
        # widget = widgets.Select(choices=[(1,"上海"),(2,"北京")]),
        widget = widgets.Select(choices=models.Classes.objects.values_list('id','title'),attrs={'class':'form-control'}),
    )

def add_student(request):
    if request.method == 'GET':
        obj = StudentForm()
        dd = models.Classes.objects.values_list('id', 'title')
        print ("keke---dd",dd)
        return render(request,'app01/add_student.html',{'obj':obj})
    else:
        obj = StudentForm(request.POST)
        if obj.is_valid():
            print ("keke_add_student",obj.cleaned_data)
            models.Student.objects.create(**obj.cleaned_data)
            return redirect("/app01/student_list/")
        else:
            print("keke_add_student3",obj.errors)
        return render(request, 'app01/add_student.html', {'obj': obj})

def edit_student(request,nid):
    if request.method == "GET":
        # row = models.Student.objects.filter(id=nid).first()
        row = models.Student.objects.filter(id=nid).values('name','email','age','cls_id').first()
        print ("aaaaaaaaaaaaaa-----row",row)
        obj = StudentForm(initial=row)

        return render(request,'app01/edit_student.html',{'nid':nid,'obj':obj})
    else:
        obj = StudentForm(request.POST)
        if obj.is_valid():
            models.Student.objects.filter(id=nid).update(**obj.cleaned_data)
            return redirect('/app01/student_list/')
        return render(request, 'app01/edit_student.html', {'nid': nid, 'obj': obj})

class TeacherForm(Form):
    tname = fields.CharField(min_length=2)
    #单选
    # xx =fields.CharField(
    #     # widget = widgets.Select(choices=models.Classes.objects.values_list('id','title'),attrs={"multiple":'multiple'}),
    #     widget = widgets.SelectMultiple(choices=models.Classes.objects.values_list('id','title')),
    # )
    #多选
    xx = fields.MultipleChoiceField(
        # choices=models.Classes.objects.values_list('id','title'),
        widget= widgets.SelectMultiple,
    )

    def __init__(self,*args,**kwargs):
        super(TeacherForm, self).__init__(*args,**kwargs)
        self.fields['xx'].widget.choices = models.Classes.objects.values_list('id','title')


def teacher_list(request):
    tea_list = models.Teacher.objects.all()
    return render(request,'app01/teacher_list.html',{'tea_list':tea_list})

def add_teacher(request):
    if request.method == "GET":
        obj = TeacherForm()
        return render(request,'app01/add_teacher.html',{'obj':obj})
    else:
        obj = TeacherForm(request.POST)
        if obj.is_valid():
            print (obj.cleaned_data)
            # models.Teacher.objects.create(tname=obj.cleaned_data['tname'])
            xx = obj.cleaned_data.pop('xx')
            row = models.Teacher.objects.create(**obj.cleaned_data)
            row.c2t.add(*xx)   #[1,2]
            return redirect('/app01/teacher_list/')
        else:
            print (obj.errors)

        return render(request, 'app01/add_teacher.html', {'obj': obj})

def edit_teacher(request,nid):
    if request.method == "GET":
        """

        """

        # row = models.Teacher.objects.filter(id=nid).values('tname','c2t__title')
        # print("keke_eidt_tea", row)
        # print("keke_eidt_tea", row.first())
        # # print("keke_eidt_tea", row)


        row = models.Teacher.objects.filter(id=nid).first()
        class_ids = row.c2t.values_list('id')
        print ("kekeaaaa,",class_ids.values_list('id'))

        id_list = list(zip(*class_ids))[0] if list(zip(*class_ids)) else []

        obj = TeacherForm(initial={'tname':row.tname,'xx':id_list})
        return render(request,'app01/edit_teacher.html',{'nid':nid,'obj':obj})
    else:
        obj = TeacherForm(request.POST)
        print ("999999900000")
        if obj.is_valid():
            print("1111111",obj.cleaned_data)
            return redirect('/app01/teacher_list/')
        else:
            return render(request,'app01/edit_teacher.html',{'nid':nid,'obj':obj})


def new_ajax(request):

    return render(request,'app01/new_ajax.html')

def add1(request):
    a1 = request.POST.get("i1")
    a2 = request.POST.get("i2")
    m = int(a1) + int(a2)
    print("keke_ajax1:%s,%s" % (a1, a2))
    return HttpResponse(m)

def add2(request):
    # import time
    # time.sleep(10)
    if request.method == "GET":
        i1 = int(request.GET.get("i1"))
        i2 = int(request.GET.get("i2"))
        print ("keke-原生ajax:%s,%s"%(i1,i2))
        return HttpResponse(i1+i2)

    else:
        print ("keke_ajaxpost_方式:",request.POST)
        print("keke_ajaxpost_方式22:", request.body)


    print ("keke:原生ajax")
    return HttpResponse("123")

def autohome(request):

    return render(request,"app01/autohome.html")

def fake_ajax(request):
    if request.method == "GET":
        return render(request,'app01/fake_ajax.html')
    else:
        print ("keke_伪造ajax:requestL:",request.POST)
        from_str = request.POST.get('user')
        list_a = quickSort([8,9,33,1,105,6])

        z = str(list_a)

        list_b = search([2, 5, 13, 21, 26, 33, 37],5)
        print ("keke990011",list_b)
        print("keke998877",from_str,z)
        return HttpResponse(from_str + z)

#定义一个快排

def quickSort(arr):   #(nlogn)
    if len(arr) < 2:
        return arr
    pivot = arr[len(arr)//2]
    left = [i for i in arr if i < pivot]
    middle = [i for i in arr if i == pivot]
    right = [i for i in arr if i > pivot]
    return quickSort(left)+quickSort(middle)+quickSort(right)

#二分法
def search(list, key):
    left = 0
    right = len(list) - 1
    while left <= right:
        mid = (left + right) //2
        if key > list[mid]:
            left = mid + 1
        elif key < list[mid]:
            right = mid -1
        else:
            print ("已经找到了---")
            return mid
    else:
        return -1

def upload(request):

    return render(request,'app01/upload.html')

import os
def yuan_ajax(request):
    if request.method == "GET":
        pass
    else:
        print ("keke_yuan_ajax",request.POST)
        print ("keke_yuan_ajax2",request.FILES)
        files_obj = request.FILES.get('fafafa')
        #写到本地
        file_path = os.path.join("static",files_obj.name)

        with open(file_path,'wb') as f:
            for chun in files_obj.chunks():
                f.write(chun)

        return HttpResponse(file_path)


# jsonp 是一种技巧，技术
#     Ajax存在：
#         访问自己域名URL
#         访问其他域名URL - 被阻止
# 浏览器遵循同源策略    Ajax跨域发送请求时，再回来时浏览器拒绝接受
# 通过jsonp 转空子
#     允许带有 src的可以访问   script标签没有禁止
def jsonp(request):

    return render(request,'app01/jsonp.html')

from django.core.paginator import Paginator

def article(request):

    search = request.GET.get('search')
    order = request.GET.get('order')

    column = request.GET.get('column')
    tag = request.GET.get('tag')

    #初始化查询集
    article_list = models.ArticlePost.objects.all()

    # 搜素查询集
        # if search:
        #     if order == "total_views":
        #         # 用 Q对象 进行联合搜索
        #         # Q(title__icontains=search)意思是在模型的title字段查询，
        #         # icontains是不区分大小写的包含，中间用两个下划线隔开。
        #         # search是需要查询的文本。多个Q对象用管道符|隔开，
        #         # 就达到了联合查询的目的。
        #         article_list = models.ArticlePost.objects.filter(
        #             Q(title__icontains=search) |
        #             Q(body__icontains=search)
        #         ).order_by('-total_views')
        #     else:
        #         article_list = models.ArticlePost.objects.filter(
        #             Q(title__icontains=search) |
        #             Q(body__icontains=search)
        #         )
        # else:
        #     search = ''
        #     if order == 'total_views':
        #         article_list = models.ArticlePost.objects.all().order_by('-total_views')
        #         order = 'total_views'
        #     else:
        #         article_list = models.ArticlePost.objects.all()
        #         order = 'normal'
    if search:
        article_list = article_list.filter(Q(title__icontains=search)|Q(body__icontains=search))

    else:
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 标签查询集
    if tag and tag != "None":
        #意思是在tag字段中过滤为tag的数据条目
        article_list = article_list.filter(tags__name__in=[tag])

    #查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')


    # 每页显示 1 篇文章
    paginator = Paginator(article_list, 6)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)

    print ("当前文章:",articles)
    contenxt = {'articles':articles,
                'order':order,
                'search':search,
                'column':column,
                'tag':tag,
                }

    return render(request,'app01/article.html',contenxt)


def article_detail(request,nid):
    # print ("keke1111:%s"%request.POST)
    # print("keke2222:%s" % request.GET)
    # print("keke333:%s" % request.method)
    #
    # print("keke333:%s" % nid)

    cur_articleobj = models.ArticlePost.objects.filter(id=nid).first()

    print("color_ppss:%s" % cur_articleobj.body)

    # print ("kbll:%s"%cur_articleobj)
    #
    # tp = cur_articleobj.total_views + 1
    #
    # print("kb222:%s" % cur_articleobj.total_views)
    #
    # print("kb333:%s" % tp)
    #
    # models.ArticlePost.objects.filter(id=nid).update(**{"total_views":tp})

    #上面是第一种更新方式

    #下面是第二种方式

    my_articleobj = models.ArticlePost.objects.get(id=nid)

    print ("gggg_obj:%s"% my_articleobj.body)

    my_articleobj.total_views += 1

    my_articleobj.save(update_fields=['total_views'])

    import markdown

    # cur_articleobj.body = markdown.markdown(cur_articleobj.body,
    #         extensions = [
    #             # 包含 缩写、表格等常用扩展
    #             'markdown.extensions.extra',
    #             # 语法高亮扩展
    #             'markdown.extensions.codehilite',
    #
    #             'markdown.extensions.toc',
    #         ])

    #另一种写法
    md = markdown.Markdown(
        extensions = [
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展
            'markdown.extensions.toc',
        ]
    )

    my_articleobj.body = md.convert(my_articleobj.body)

    # 取出文章评论
    comments = Comment.objects.filter(article=nid)

    comment_form = CommentForm()


    context = {'article_obj':my_articleobj,'toc':md.toc,'comments':comments,'comment_form':comment_form,}

    return render(request,'app01/detail.html',context)

@login_required(login_url='/normal/login/')
def article_create(request):
    #判断用户是否提交数据
    if request.method == "POST":

        print("mu---article_post_from156：%s" % request.FILES)

        article_post_from = ArticlePostForm(request.POST,request.FILES)

        # print ("article_post_from:",article_post_from)

        print("mu---article_post_from：%s"%request.POST)

        print("mu---article_post_from33：%s"%request.FILES)


        if article_post_from.is_valid():
            print("mu---article_post_from222：%s" % article_post_from.cleaned_data)

            # print("keke---------------shenme00000",article_post_from)


            new_article = article_post_from.save(commit=False)


            print ("7788999",request.user)

            new_article.author = UserProfile.objects.filter(username=request.user).first()

            #新增的代码
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])

            new_article.save()

            # 新增代码，保存 tags 的多对多关系
            article_post_from.save_m2m()

            #如果提交的表单使用了commit=False选项，则必须调用save_m2m()才能正确的保存标签，就像普通的多对多关系一样


            return redirect(reverse('app01:article'))
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    else:
        # https: // www.dusaiphoto.com / article / 22 /
        article_post_form = ArticlePostForm()

        columns = ArticleColumn.objects.all()

        context = {'article_post_form':article_post_form,'columns':columns}

        # use_admin_list = UserProfile.objects.all()
        # for use_obj in use_admin_list:
        #     print ("keke222",use_obj.id)
        #     print("keke222", use_obj.username)

        return render(request, 'app01/create.html', context)


def article_delete(request,id):
    if request.method == "POST":
        article_obj = models.ArticlePost.objects.filter(id=id).first()
        article_obj.delete()

        return redirect(reverse('app01:article'))
    else:

        return HttpResponse('仅允许post请求')

def article_update(request,id):
    article_obj = models.ArticlePost.objects.filter(id=id).first()

    if request.method == "POST":
        article_post_form = ArticlePostForm(request.POST)

        if article_post_form.is_valid():
            print ("keke:article_post_form",article_post_form.cleaned_data)

            # models.ArticlePost.objects.filter(id=id).update(**article_post_form.cleaned_data)

            article_obj.title = article_post_form.cleaned_data['title']
            article_obj.body = article_post_form.cleaned_data['body']

            if article_post_form.cleaned_data['column'] != 'none':
                #保存文章栏目
                article_obj.column = ArticleColumn.objects.get(id=article_post_form.cleaned_data['column'].id)
            else:
                article_obj.column = None

            if request.FILES.get('avatar'):
                article_obj.avatar = request.FILES.get('avatar')

            if (request.POST.get('tags')):

                article_obj.tags.set(*request.POST.get('tags').split(','),clear=True)

            article_obj.save()
            msg = article_obj.id
            return redirect('/app01/article_detail/%s'%msg)

        else:
            print ("article_post_form--内容有误",article_post_form.errors)

            return HttpResponse("表单内容有误，请重新填写")

            # msg = article_obj.id
            # return redirect('/app01/article_update/%s' % msg,**{'article_post_form':article_post_form})
    else:

        article_post_form = ArticlePostForm()

        columns = ArticleColumn.objects.all()

        context = {'article_obj':article_obj,'article_post_form':article_post_form,'columns':columns}

        return render(request,'app01/update.html',context)



class ArticleListView(View):
    """处理GET请求"""
    def get(self,request):
        articles = models.ArticlePost.objects.all()
        context = {'articles':articles}
        return render(request,'app01/article.html',context)

#点赞数 +1
class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        print("keke--aa11",args)
        print("keke--aa22",kwargs)

        article = models.ArticlePost.objects.get(id = args[0])
        article.likes += 1
        article.save()
        return HttpResponse('success')
    def get(self,request,*args,**kwargs):
        print("keke--aa13", args[0])
        print("keke--aa23", kwargs)
        print("keke--aa444", request.GET)

        return HttpResponse('success')




