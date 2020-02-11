# -*- coding: utf-8 -*-
from .models import *
from django.contrib.contenttypes.models import ContentType

#自定义的函数，不是视图
def get_like_count(obj):
    content_type = ContentType.objects.get_for_model(obj)


    like_count, created = LikeCount.objects.get_or_create(content_type=content_type,object_id=obj.pk)