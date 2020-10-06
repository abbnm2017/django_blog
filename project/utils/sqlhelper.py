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

def create(sql,args):
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='123456',db='blog')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    conn.commit()
    last_row_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return last_row_id


class SqlHelper(object):
    def __init__(self):
        #读配置文件
        self.connect()
    def connect(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='blog')
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def get_list(self,sql,args):
        self.cursor.execute(sql,args)
        result = self.cursor.fetchall()
        return result

    def get_one(self,sql,args):
        self.cursor.execute(sql,args)
        result = self.cursor.fetchone()
        return result
    def modify(self,sql,args):
        self.cursor.execute(sql,args)
        self.conn.commit()
    def  create(self,sql,args):
        self.cursor.execute(sql,args)
        self.conn.commit()
        return self.cursor.lastrowid
    def multiple_modify(self,sql,args):
        self.cursor.executemany(sql,args)
        # self.cursor.executemany("insert into bd(id,name)value(%s,%s)",[(1,'alex'),(2,'eric')])
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

## obj = SqlHelper()
## obj.connect()
## obj.