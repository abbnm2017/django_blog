# -*- coding:utf-8 -*-
import asyncio
import urllib.request

url_imglist = [
	'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=4858554,2092434492&fm=26&gp=0.jpg',
	'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=1115057027,1261114857&fm=26&gp=0.jpg',
	'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=1578307669,1098408709&fm=26&gp=0.jpg',
]


for i_url in url_imglist:
	img_pic = urllib.request.urlopen(i_url)
	print ("keke111:%s"%img_pic)
	print("keke111:%s" % img_pic.read())



#去生成或获取一个时间循环
# print ("keke11",loop)

#将任务放到'任务列表'




async def haha():
	print ("jaja")
	return

alist = haha()

# print (alist)

loop = asyncio.get_event_loop()
loop.run_until_complete(alist)



#print ("keke11",asyncio)


def GetNearNumber(n, iterobj, down = True):
	v = None
	r = None
	if down == True:
		for i in iterobj:
			if i <= n:
				m = n - i
				if v == None or m <= v:
					v = m
					r = i
	elif down == False:
		for i in iterobj:
			if i >= n:
				m = i - n
				if v == None or m <= v:
					v = m
					r = i
	else:
		for i in iterobj:
			m = abs(i - n)
			if v == None or m <= v:
				v = m
				r = i
	return r
