# -*- coding: utf-8 -*-
#作用就是向网易云信发送请求，帮助后台发送短信给客户
# import requests
import hashlib
import json

from time import time

def util_sendmsg(mobile):
    url = 'https://api.netease.im/sms/sendcode.action'

    data = {'mobile':mobile}

    #4部分组成  headers: AppKey  Nonce CurTime CheckSum

    AppKey = 'cb8bd3677a564ce3a542f4485f2ff0db'

    Nonce = '843jdfsdsadas85451v23694'

    CurTime = str(time())

    AppSecret = 'e4abb82ef3d2'

    content = AppSecret + Nonce + CurTime

    CheckSum = hashlib.sha1(content.encode('utf-8')).hexdigest()


    headers = {'AppKey':AppKey, 'Nonce':Nonce,'CurTime':CurTime,'CheckSum':CheckSum}

    response = requests.post(url, data, headers = headers)

    #json
    str_result = response.text   #获取响应体

    json_result = json.loads(str_result)   #转成json

    return json_result