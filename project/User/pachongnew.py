# -*- coding: utf-8 -*-
import re
import os
import urllib
# import urllib2
import shutil
from PIL import Image
from .models import PcImgK
import random
import urllib.request
import asyncio
import aiohttp

global_imglist = []
new_path = ""

# url = ('https://image.baidu.com/search/acjson?'
#        'tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&'
#        'queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&'
#        'word={word}&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&'
#        'pn={pn}&rn=30&gsm=5a&1516945650575=')

url = ('https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word={word}&pn={pn}')


def getHtml(url):
    #python2.7
        # page = urllib.urlopen(url)
    #python 3
    print ("kekezzz",url)
    req = urllib.request.Request(url=url, headers={'UserAgent': 'Mozilla/5.0 (Windows NT 10.0;Win64;x64)AppleWebKit / 537.36(KHTML, likeGecko)Chrome / 71.0.3578.80Safari / 537.36'})
    page = urllib.request.urlopen(req)



    # print ("mypage33",page)
    html = page.read()
    # print("mypage11", html)
    return html

def getImg(html):
    # reg = r'"objURL":"(.*?)"'
    reg = '"thumbURL":"(.+?\.jpg)"'
    imgre = re.compile(reg)
    # print ("keke1222:%s"%html.decode('utf-8'))
    print (imgre)
    #python 2
    # imglist = re.findall(imgre,html)
    #python3
    imglist = re.findall(imgre, html.decode('utf-8'))
    l = len(imglist)
    # print ("7788:%s"%imglist)

    global global_imglist
    global_imglist = imglist
    return imglist

# def downLoad(urls,path):
#     index = 1
#     PcImgK.objects.all().delete()
#     for url in urls:
#         if index > 20:
#             break
#         print("Downing:",url)
#         try:
#             res = urllib2.Request(url)
#             if str(res.status_code)[0] == "4":
#                 print("download failed!", url)
#                 continue
#         except Exception as e:
#             print("download failed!",url)
#
#         suijishu = random.randint(0,1000000000)  #新增加随机数
#
#         filename = os.path.join(path,str(index) +str(suijishu)+".jpg")
#
#         #python2
#         # urllib.urlretrieve(url,filename)
#         #python3
#         urllib.request.urlretrieve(url, filename)
#
#         img = Image.open(filename)
#
#
#         print("keke_image666:%s"%filename)
#
#         print ("558:%s"%img)
#         # 切割图片
#         resized_image = img.resize((500, 500), Image.ANTIALIAS)
#
#
#         resized_image = resized_image.convert("RGB")  #PNG格式转换成的四通道转成RGB的三通道
#
#         resized_image.save(filename)
#
#         kekename = os.path.join("img/", str(index) + str(suijishu)+".jpg")
#
#         new_img = PcImgK(img = kekename,name = "")
#
#         new_img.save()
#         index += 1

async def fetch(session,url,path):
    # print ("发送请求:%s,%s"%(url,session))
    async with session.get(url,verify_ssl=False) as response:
        content = await response.content.read()
        # print ("keke-img:%s"%content)
        index = url.rsplit('.')[-1][0:2]
        suijishu = random.randint(0, 1000000000)  # 新增加随机数
        filename = os.path.join(path, str(index) + str(suijishu) + ".jpg")

        with open(filename,"wb") as file_object:
            file_object.write(content)

        img = Image.open(filename)

        print("keke_image666:%s" % filename)

        print("558:%s" % img)

        # 切割图片
        resized_image = img.resize((500, 500), Image.ANTIALIAS)

        resized_image = resized_image.convert("RGB")  # PNG格式转换成的四通道转成RGB的三通道

        resized_image.save(filename)

        kekename = os.path.join("img/", str(index) + str(suijishu) + ".jpg")

        new_img = PcImgK(img=kekename, name="")

        new_img.save()

#携程
async def downLoad(urls,path):
    # print("keke_url_list1:",urls)
    print("keke_url_list2:", len(urls))
    #打乱，取前20
    random.shuffle(urls)
    urls = urls[:20]

    print("keke_url_list3:", len(urls))
    async with aiohttp.ClientSession() as session:
        loop = asyncio.get_event_loop()
        tasks = [loop.create_task(fetch(session,url,path)) for url in urls]

        await asyncio.wait(tasks)

    # PcImgK.objects.all().delete()



    return
    index = 1
    for url in urls:
        if index > 20:
            break
        print("Downing:",url)
        try:
            res = urllib2.Request(url)
            if str(res.status_code)[0] == "4":
                print("download failed!", url)
                continue
        except Exception as e:
            print("download failed!",url)

        suijishu = random.randint(0,1000000000)  #新增加随机数

        filename = os.path.join(path,str(index) +str(suijishu)+".jpg")

        #python2
        # urllib.urlretrieve(url,filename)
        #python3
        urllib.request.urlretrieve(url, filename)

        img = Image.open(filename)


        # print("keke_image666:%s"%filename)

        # print ("558:%s"%img)
        # 切割图片
        resized_image = img.resize((500, 500), Image.ANTIALIAS)


        resized_image = resized_image.convert("RGB")  #PNG格式转换成的四通道转成RGB的三通道

        resized_image.save(filename)

        kekename = os.path.join("img/", str(index) + str(suijishu)+".jpg")

        new_img = PcImgK(img = kekename,name = "")

        new_img.save()
        index += 1

# url = ('https://image.baidu.com/search/acjson?'
#        'tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&'
#        'queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&'
#        'word={word}&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&'
#        'pn={pn}&rn=30&gsm=5a&1516945650575=')

url = ('https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word={word}&pn={pn}')

def geturls(num, online_word):
    print ("9988:",online_word)
    print ("kekeonline:%s"%online_word)
    #这个word 一定要转成utf-8,转gbk就凉了
    # s1 = unicode(online_word, "cp936")

    # print ("kekeonline2:%s"%s1)
    # #

    # p1 = s1.encode("utf-8")
    import sys
    print (sys.stdin.encoding)


    keke1 = online_word.encode('utf-8')

    print("keke____222:%s"%keke1)

    # keke2 = online_word.decode('UTF-8').encode('GBK')

    # print("keke____111:%s" % keke2)

    # p1 = online_word
    #
    #python2
        # word = urllib.quote(keke1)
    #python3
    word = urllib.request.quote(keke1)
    # word = "%E6%9D%A8%E5%B9%82"
    urls = []
    pn = (num // 30 + 1) * 30
    for i in range(30, pn + 1, 30):

        urls.append(url.format(word=word, pn=i))
    return urls

def Run(word,num):
    # html = getHtml("https://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gbk&word=%B1%ED%C7%E9%B0%FC&fr=ala&ori_query=%E8%A1%A8%E6%83%85%E5%8C%85&ala=0&alatpl=sp&pos=0&hs=2&xthttps=111111")
    path = "static/purge/img"

    # word = "杨幂"
    urlss = geturls(2,word)
    print("sss,",urlss)

    html = getHtml(urlss[0])

    shutil.rmtree(path)
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)


    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)


    # downLoad(getImg(html),path)

    getImg(html)

    global new_path

    new_path = path


# if __name__ == '__main__':
#     print ("keke--1234")
#     # loop = asyncio.get_event_loop()
#     # loop.run_until_complete(downLoad(getImg(html), path))

def Start():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()

    loop.run_until_complete(downLoad(global_imglist, new_path))

