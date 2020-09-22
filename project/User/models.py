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
    name = models.CharField(max_length=100)
    classes = models.CharField(max_length=100)










