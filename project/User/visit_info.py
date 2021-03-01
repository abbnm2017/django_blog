# -*- coding: utf-8 -*-
from .models import *
from django.utils import timezone

#自定义的函数，不是视图
def change_info(request):              #修改网站访问量和访问ip等信息  # 每一次访问，网站总访问次数加一
    print ("keke_ip1:%s"%request)
    count_nums = VisitNumber.objects.filter(id=1)

    print ("keke_ip_ssss:%s"%count_nums)

    if count_nums:
        count_nums = count_nums[0]
        count_nums.count += 1
    else:
        count_nums = VisitNumber()
        count_nums.count = 1

    print ("keke_ip2:%s" % count_nums)
    count_nums.save()

    print ("keke_ip3:%s" % request.META)

    # 记录访问ip和每个ip的次数
    if 'HTTP_X_FORWARDED_FOR' in request.META: #获取ip
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0] #所以这里是真实的ip
        print ("keke_llllllTrue")
    else:
        client_ip = request.META['REMOTE_ADDR']  #这里获得代理ip
        print ("keke_llllllFalse")

    print("keke_my_ip:%s"%client_ip)

    ip_exist = Userip.objects.filter(ip=str(client_ip))
    print ("keke_ip4:%s" % ip_exist)

    if ip_exist:  #判断是否存在该ip
        uobj = ip_exist[0]
        uobj.count += 1
    else:
        uobj = Userip()
        uobj.ip = client_ip
        uobj.count = 1

    print ("keke_ip888:%s" % uobj)
    print ("keke_ip999:%s" % uobj.count)
    uobj.save()

    #增加今日访问次数
    date = timezone.now().date()
    today = DayNumber.objects.filter(day=date)

    print ("keke_ip5:%s" % date)

    print ("keke_ip6:%s" % today)

    if today:
        temp = today[0]
        temp.count += 1
    else:
        temp = DayNumber()
        temp.dayTime = date
        temp.count = 1
    temp.save()

    print ("keke_ip77:%s" % temp)

    return temp.count, count_nums.count