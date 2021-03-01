# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser

from django.db import models

from django.utils import timezone

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.conf import settings
# Create your models here.


class UserProfile(AbstractUser):

    mobile = models.CharField(max_length=11, verbose_name='手机号码', unique= True)
    icon = models.ImageField(upload_to='uploads/%Y/%m/%d')

    class Meta:
        db_table = 'userprofile'
        verbose_name = "用户表"
        verbose_name_plural = verbose_name

#f访问网站的ip地址和次数
class Userip(models.Model):
    ip = models.CharField(verbose_name='IP地址',max_length=30)   #ip地址
    count= models.IntegerField(verbose_name='访问次数',default=0) #该ip访问次数
    class Meta:
        verbose_name= '访问用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip

#网站总访问次数
class VisitNumber(models.Model):
    count = models.IntegerField(verbose_name='网站访问总次数',default=0) #网站访问总次数
    class Meta:
        verbose_name = '网站访问总次数'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.count)

#单日访问量统计
class DayNumber(models.Model):
    day=models.DateField(verbose_name='日期', default= timezone.now)
    count = models.IntegerField(verbose_name='网站访问次数',default=0) #网站访问次数
    class Meta:
        verbose_name = '网站日访问量统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.day)

#留言板
class MessageBoard(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=255)


#点赞
class LikeCount(models.Model):
    content_type = models.ForeignKey(ContentType,on_delete = models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

    liked_num = models.IntegerField(default=0)

class LikeRecord(models.Model):
    content_type = models.ForeignKey(ContentType,on_delete = models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

    like_time = models.DateTimeField(auto_now_add = True)


class ImgK(models.Model):
    img = models.ImageField(upload_to='img')
    name = models.CharField(max_length = 1000)


class PcImgK(models.Model):
    img = models.ImageField(upload_to='keke')
    name = models.CharField(max_length=1000)


class student(models.Model):
    name = models.CharField(max_length=1000)
    class_id = models.IntegerField()

class allclass(models.Model):
    cls_title = models.CharField(max_length=1000)

class teacher(models.Model):
    teacher_name = models.CharField(max_length=1000)

class tea2class(models.Model):
    teacher_id = models.IntegerField()
    class_id = models.IntegerField()

class testdata(models.Model):
    name = models.CharField(max_length=64)

#多表操作
class testinfo(models.Model):
    nid = models.BigAutoField(primary_key=True)
    user = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    age = models.IntegerField(default=1)
    ug = models.ForeignKey("testdata",on_delete=models.CASCADE,null=True)

#专门用来进行测试的表格
class abbnm(models.Model):
    md = models.IntegerField(default=1)

#跨表
# 正向:
# 1.q = testinfo.objects.all().first()
#   q.ug.title()
# 2. testinfo.objects.values('nid','ug_id','ug__title')
# 3. testinfo.objects.values_list('nid','ug_id','ug__title')
# 反向:
# 1.obj = testdata.objects.all().first()
#     result = obj.testinfo_set.all()    #queryset([testinfo对象])
#   2.
#     v = testdata.objects.values('id','name')
#     v = testdata.objects.values('id','name','testinfo_set__password')

class Boy(models.Model):
    name = models.CharField(max_length=32)
    # m = models.ManyToManyField('Girl')   #帮我新建一个表
    m = models.ManyToManyField('Girl',through='Love',through_fields=('b','g',))


class Girl(models.Model):
    nick = models.CharField(max_length=32)


class Love(models.Model):
    b = models.ForeignKey('Boy',on_delete=models.CASCADE)
    g = models.ForeignKey("Girl",on_delete=models.CASCADE)

    #联合唯一索引
    class Meta:
        unique_together = [
            ('b','g')
        ]

# django 可以自动生成 class Love表


class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    email = models.EmailField()
    # f = models.FileField()
    c_time = models.DateTimeField(null=True)

    color_list =  (
        (1,"黑色"),
        (2,"白色"),
        (3,"蓝色"),
    )
    color = models.IntegerField(choices=color_list)
    #直接通过
    # models.UserInfo.objects.create()   ...是不受emailfield的影响
        #--ModelForm 不能直接通过
    # 会影响Django自带的管理工具admin

    # 字符串
    #     models.EmailField
    #     models.IPAddressField()
    #     models.URLField()
    #     models.SlugField()
    #
    #     models.UUIDField()
    #     models.FilePathField()
    #     models.FileField()
    #     models.ImageField()
    #     models.CommaSeparatedIntegerField()
    # 时间类
    #     models.DateTimeField()

#制作相亲数据
class MarryBoy(models.Model):
    nickname = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)

class MarryGirl(models.Model):
    nickname = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)

class MarryB2G(models.Model):
    b = models.ForeignKey(to='MarryBoy',to_field='id',on_delete=models.CASCADE)
    g = models.ForeignKey(to='MarryGirl', to_field='id',on_delete=models.CASCADE)

#能否把两张表结合成一张表

class MarryBoth(models.Model):
    nickname = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)

    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.IntegerField(choices=gender_choices)


class U2U(models.Model):
    g = models.ForeignKey("MarryBoth",on_delete =models.CASCADE, related_name='boys')
    b = models.ForeignKey("MarryBoth", on_delete=models.CASCADE, related_name='girls')

#评论表
class Comment(models.Model):
    news_id = models.IntegerField()    #新闻id
    content = models.CharField(max_length=32)  #评论内容
    user = models.CharField(max_length=32)          #评论者
    reply = models.ForeignKey('Comment',null=True,blank=True,related_name='xxxx',on_delete=models.CASCADE)
"""
评论的自增id  新闻ID                                                                  reply_id(回复者id)
   1            1 别比比  root     代表root这个人给这个1 号新闻id 评论了 别比比           null
   2            1 就比比  root     代表root这个人评论两条                                null
   3            1 瞎比比  shaowei   代表shaowei这个人评论                                null
   4            2 写的正好 root     代表shaowei这个人评论 2号新闻id                       null
   5            1  拉倒吧  有清兵                                                         2
   6            1  拉倒吧1  xxxx                                                          2
   7            1  拉倒吧2  xxxx                                                          5
"""
"""
新闻1
    别比比
    就比比
        -拉倒吧
            -拉倒吧2
        -拉倒吧1
    瞎比比
新闻2
    写的正好
"""



