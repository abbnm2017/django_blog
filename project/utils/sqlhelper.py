import pymysql


def get_list(sql,args):
    conn = pymysql.connect(host='127.0.0.1',port=3306, user='root', passwd='123456',db = "blog" )
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_one_list(sql,args):
    conn = pymysql.connect(host='127.0.0.1',port=3306, user='root', passwd='123456',db = "blog" )
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def modify(sql,args):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db="blog")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    conn.commit()
    cursor.close()
    conn.close()


def get_now_time():
    #获取当前时间
    from django.utils import timezone
    import pytz
    import datetime
    tz = pytz.timezone('Asia/Shanghai')

    #返回时间格式的字符串
    now_time = timezone.now().astimezone(tz = tz)

    now_time_str = now_time.strftime("%Y.%m.%d %H:%M:%S")

    #返回datetime格式的时间
    now_time = timezone.now().astimezone(tz=tz).strftime("%Y.%m.%d %H:%M:%S")

    now = datetime.datetime.strptime(now_time, "%Y.%m.%d %H:%M:%S")

    return now_time_str