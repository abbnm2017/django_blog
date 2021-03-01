# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

#把我自己的表格注册在这
from User import models
admin.site.register(models.testinfo)
admin.site.register(models.UserInfo)
