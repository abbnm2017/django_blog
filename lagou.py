# -*- coding: utf-8 -*-
"""
" Author: keke
" Data: 2020/8/27
" Desc: 拉钩爬虫jd
" 2021.7.19. keke20210719 创建分支
" 第二次测试....
"""
import requests
import math
import time
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup


cookies2 = {
'Cookie':
    "user_trace_token=20200824112701-4a53a6c1-fefc-4dd1-b88b-6f39b381043d; _ga=GA1.2.830222859.1598239619; " \
"_gid=GA1.2.744548583.1598239619; LGUID=20200824112701-83c4e1ae-5c73-4951-871a-989f592427cf; " \
"gate_login_token=23cb5a2a3d39ed68ded0b3ef46fc3f5529490eb827951312; LG_LOGIN_USER_ID=0a89c67ea6d45a96acb5e84ba63566c556330c9ea212d4b1; " \
"LG_HAS_LOGIN=1; privacyPolicyPopup=false; " \
"index_location_city=%E6%B7%B1%E5%9C%B3; " \
"sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221741e8139985d-0a129b919cfd77-58143518-1296000-1741e813999a6e%22%2C%22%24device_id%22%3A%221741e8139985d-0a129b919cfd77-58143518-1296000-1741e813999a6e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; " \
"_putrc=596E1CBC48950ACF; login=true; " \
"unick=%E6%B1%AA%E5%AD%90%E7%85%9C; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1598239620,1598239653,1598240249,1598407627; " \
"_gat=1; PRE_UTM=; PRE_HOST=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F5724657.html; " \
"LGSID=20200826173722-fa0c446f-c66e-43c7-a989-f8779e99ce05; PRE_SITE=; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1598434640;" \
" LGRID=20200826173723-752dea24-4d38-4b9c-a652-0d715d2d1bc1; X_HTTP_TOKEN=f85ef9ec3fa107895464348951f376ce1546cb4314"
}



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Host': 'www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
    'X-Anit-Forge-Code': '0',
    'X-Anit-Forge-Token': 'None',
    'X-Requested-With': 'XMLHttpRequest'
}


cookies = {
    'Cookie': 'user_trace_token=20170901085741-8ea70518-8eb0-11e7-902f-5254005c3644;'
              'LGUID=20170901085741-8ea7093b-8eb0-11e7-902f-5254005c3644; '
              'index_location_city=%E6%B7%B1%E5%9C%B3; SEARCH_ID=7277bc08d137413dac2590cea0465e39; '
              'TG-TRACK-CODE=search_code; JSESSIONID=ABAAABAAAGGABCBF0273ED764F089FC46DF6B525A6828FC; '
              'PRE_UTM=; PRE_HOST=; '
              'PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_java%3Fcity%3D%25E6%25B7%25B1%25E5%259C%25B3%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; '
              'PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F3413383.html; _gat=1; _'
              'gid=GA1.2.807135798.1504227456; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504227456; '
              'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504252636; _ga=GA1.2.1721572155.1504227456; '
              'LGSID=20170901153335-dd437749-8ee7-11e7-903c-5254005c3644; '
              'LGRID=20170901155728-336ca29d-8eeb-11e7-9043-5254005c3644',
}


#增加动态cooies 我说TM的 怎么爬拉钩怎么有的爬的下来，有的爬的是空的，原因是之前一直用的是固定的cookies，被反爬虫机制拦掉了、
#模仿浏览器登录   独家经验
class Spider(object):
    def __init__(self):
        self.header_lagou = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'Host': 'www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
            'X-Anit-Forge-Code': '0',
            'X-Anit-Forge-Token': 'None',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Origin': 'https://www.lagou.com',
        }

        self.myurl = "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput="

        self.s = requests.Session()

        self.s.headers = self.header_lagou


    def get_my_cookies(self):
        self.s.get(self.myurl,headers = self.s.headers,timeout=3)
        cookie = self.s.cookies
        print ("900135558:",cookie)
        return cookie



def get_json(url, num):
    """
    从指定的url中通过requests请求携带请求头和请求体获取网页中的信息,
    :return:
    """
    url1 = 'https://www.lagou.com/jobs/list_python%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88?labelWords=&fromSearch=true&suginput='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {
        'first': 'true',
        'pn': num,
        'kd': 'python'}
    s = requests.Session()
    print('建立session：', s, '\n\n')
    s.get(url=url1, headers=headers, timeout=3)
    cookie = s.cookies
    print('获取cookie：', cookie, '\n\n')
    res = requests.post(url, headers=headers, data=data, cookies=cookie, timeout=3)
    res.raise_for_status()
    res.encoding = 'utf-8'
    page_data = res.json()
    print('请求响应结果：', page_data, '\n\n')
    return page_data


def get_page_num(count):
    """
    计算要抓取的页数，通过在拉勾网输入关键字信息，可以发现最多显示30页信息,每页最多显示15个职位信息
    :return:
    """
    page_num = math.ceil(count / 15)
    if page_num > 30:
        # return 30
        return 1
    else:
        # return page_num
        return 1


def get_page_info(jobs_list):
    """
    获取职位
    :param jobs_list:
    :return:
    """
    page_info_list = []
    idbx = 0
    for i in jobs_list:  # 循环每一页所有职位信息
        job_info = []
        job_info.append(i['companyFullName'])
        job_info.append(i['companyShortName'])
        job_info.append(i['companySize'])
        job_info.append(i['financeStage'])
        job_info.append(i['district'])
        job_info.append(i['positionName'])
        job_info.append(i['workYear'])
        job_info.append(i['education'])
        job_info.append(i['salary'])
        job_info.append(i['positionAdvantage'])
        job_info.append(i['industryField'])
        job_info.append(i['firstType'])
        job_info.append(i['companyLabelList'])
        job_info.append(i['secondType'])
        job_info.append(i['city'])

        #新增jd   (这里要考虑动态更新cookies)
        positionId = i['positionId']
        #
        # positionId = 6603169

        detail_url = 'https://www.lagou.com/jobs/{}.html'.format(positionId)


        # if idbx % 2 == 0:
        #     response = requests.get(url=detail_url, headers=headers, cookies=cookies2)
        # else:
        #     response = requests.get(url=detail_url, headers=headers, cookies=cookies)

        my_cookies = Spider().get_my_cookies()
        response = requests.get(url=detail_url, headers=headers, cookies=my_cookies, timeout = 3)
        response.encoding = 'utf-8'

        time.sleep(2)

        print("keke77333111", response)

        print("keke77111--content", response.content)

        print("keke_jdiddd",positionId)

        tree = etree.HTML(response.text)

        detail_soup = BeautifulSoup(response.content, 'html.parser')
        # detail_page_dd = detail_soup.find('dd', class_='job_bt').get_text()
        detail_page_dd = ""
        if detail_soup.find('dd', class_='job_bt') :
            detail_page_dd = detail_soup.find('dd', class_='job_bt').get_text()




        print ("keke9988333",detail_page_dd)

        # desc = tree.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')

        # desc = tree.xpath('//dl[@class="job_detail"]//text()')
        #
        # # desc = tree.xpath('//dl[@class="job_detail"]//div[1]/br')
        #

        # desc = tree.xpath('//dl[@class="job_detail"]//text()')

        #################################################################################

        # desc = tree.xpath("//html/body/div[@id='container']/div[@class='content_l fl']/dl[@class='job_detail']"
        #                   "/dd[@class='job_bt']/div/p/text()")
        #
        # if len(desc) <=0:
        #     desc = tree.xpath("//html/body/div[@id='container']/div[@class='content_l fl']/dl[@class='job_detail']"
        #                       "/dd[@class='job_bt']/div/br/text()")


        ####################################################################################

        # desc = tree.xpath("//html/body/div[@id='container']/div[@class='content_l fl']/dl[@class='job_detail']"
        #                   "/dd[@class='job_bt']/div")

        # print("keke_log", desc)
        #
        # for i in desc:
        #
        #     print ("keke9999",i.xpath('./text'))


        profess_list = []
        # print("keke10086",desc)
        # txt = ""
        # if len(desc) > 0:
        #     for tp in desc:
        #         print("keke778899", tp)
        #         txt += tp.text
        #
        # print("keke7788", txt)
        # print ("------------------------------------------------")


        job_info.append(detail_page_dd)
        page_info_list.append(job_info)
        idbx += 1
    return page_info_list


def main():
    # url = ' https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false'
    first_page = get_json(url, 1)

    print ("keke123:%s"%first_page['content']['positionResult'])
    total_page_count = first_page['content']['positionResult']['totalCount']

    #总共多少个职位


    num = get_page_num(total_page_count)

    print ("keke分成多少：%s"%(num))
    total_info = []
    time.sleep(10)
    print("python开发相关职位总数:{},总页数为:{}".format(total_page_count, num))
    for num in range(1, num + 1):
        # 获取每一页的职位相关的信息
        page_data = get_json(url, num)  # 获取响应json
        jobs_list = page_data['content']['positionResult']['result']  # 获取每页的所有python相关的职位信息

        print ("keke9999:%s"%jobs_list)


        page_info = get_page_info(jobs_list)
        print("每一页python相关的职位信息:%s" % page_info, '\n\n')
        total_info += page_info
        print('已经爬取到第{}页，职位总数为{}'.format(num, len(total_info)))
        time.sleep(20)
        # 将总数据转化为data frame再输出,然后在写入到csv各式的文件中
        df = pd.DataFrame(data=total_info,
                          columns=['公司全名', '公司简称', '公司规模', '融资阶段', '区域', '职位名称', '工作经验', '学历要求', '薪资', '职位福利', '经营范围',
                                   '职位类型', '公司福利', '第二职位类型', '城市', 'JD'])
        df.to_csv('Python_development_engineer.csv', encoding = "gb18030", index=False)
        print('python相关职位信息已保存')


if __name__ == '__main__':
    main()