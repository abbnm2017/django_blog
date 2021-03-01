






media文件 �?文件上传的文�? --------2019�?�?1

模型�?FileField(任何文件)      ImageField(只能是图�?

FileField(upload_to = '表示文件上传的路�?uploads/%Y/%m')

此路径是基于 media_root 指明的路�?

在setting.py 文件中配置：
MEDIA_URL = '/static/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

static
    -----media
            -----uploads
                    ----2019
                          ----05
                               -----文件�?


模板中如果想引用上传的文�?并显�?
就需要在settings.py ------> TEMPLATES ------>    'context_processors': [--'django.template.context_processors.media',


系统默认用户的继承使�?
1.密续继承AbstractUser
class UserProfile(AbstractUser):

    mobile = models.CharField(max_length=11, verbose_name='手机号码', unique= True)
    icon = models.ImageField(upload_to='uploads/%Y/%m/%d')

    class Meta:
        db_table = 'userprofile'
        verbose_name = "用户�?
        verbose_name_plural = verbose_name

2.必须修改settings.py
    添加:
    #如果用户继承了AbstractUser,修改auth_user的模�?
    AUTH_USER_MODEL = 'User.UserProfile'
3.然后执行迁移和同�?


#第三�? 46min
#第qi�? 14min

使用：Form �?ModelForm

Form比较灵活需要自己定义各个要验证的字�?
Form使用:
class UserRegisterForm(Form):
    username = forms.CharField()



session 的使�?
设置
    request.session['key'] = value
取�?
    value = request.session.get(key)


2020�?�?
�?models.py 中定义数据库中数据名和字�?
1.主键可以不定义， 默认会生成一个id主键�?当然也可以自定义主键
注意�?
1�?必须写default�?
2�?verbose_name 相当于起一个别名，方便阅读
3�?如果是字符字段，必须写最大长�?
4�?定义主键要写关键�?primary_key

2. 你可以在任意一个模型类中使用meta类， 用来设置一些与特定模型相关的选项
 其中ordering值的类型必须是一个元组或者列�?
 db_table用来自定义表�?

 ORM （object Relation Mapping）模�?
 对象关系映射
 是一种为了解决面向对象与关系数据库存在的互不匹配的现象的技�?

 ORM中默认的数据管理器是objects�?常用的方法有all(), filter(), delete()
 1. all() 将所有数据返回成一个queryset类型，可遍历操作
 2. filter() 取出指定条件值，如filter_message = UserMessage.objects.filter(name='jack',address = '西安'),同样可进行遍历操�?

sudo fuser -k 80/tcp   #关闭端口占用

pip install --upgrade setuptools

python -m pip install --upgrade pip


#Ctrl + Alt + Space  ���ٵ��������� (pycharm)


