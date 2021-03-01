"""
author：keke
datetime:2020.1.6.14:14
desc: 线程
"""
import threading
import time

# 线程是程序中工作的最小单元

# def show(arg):
#     time.sleep(1)
#     print ('thread' + str(arg))
#
# for i in range(10):
#     t = threading.Thread(target =show, args=(i,))
#     t.start()
#
# print ('main thread stop')


# class MyThread(threading.Thread):
#     def __init__(self,num):
#         threading.Thread.__init__(self)
#         self.num = num
#
#     def run(self):  #定义每个线程要运行的函数
#         print("running on number:%s"%self.num)
#         time.sleep(3)
#
# if __name__ == "__main__":
#     t1 = MyThread(1)
#     t2 = MyThread(2)
#     t1.start()
#     t2.start()


#线程加锁  (线程调度随机)   （多个线程同时修改同一条数据是可能出现脏数据，所以出现了线程锁，同一时刻允许一个线程执行操作）
"""
lock = threading.RLock()
lock.acquire()
lock.release()
t = threading.Thread(target="",args=())
t.start()
"""


# gl_num = 0
#
# lock = threading.RLock()    #
#
# def Func(args):
#     # lock.acquire()
#     # global gl_num
#     # gl_num += 1
#     # time.sleep(1)
#     # print (gl_num)
#     # lock.release()
#     lock.acquire()
#     time.sleep(1)
#     print ("cue_num----"+str(args) +"\n")
#     lock.release()
#
# for i in range(10):
#     t = threading.Thread(target=Func,args=(i,))
#     t.start()


#信号量 semaphore 允许一定数量的线程更改数据 最多允许(算是互斥锁)

# def func(arg):
#     semaphore.acquire()
#     time.sleep(1)
#     print("run the thread :%s"%arg)
#     semaphore.release()
#
#
# if __name__ == "__main__":
#     num = 0
#     semaphore = threading.BoundedSemaphore(5)
#     for i in range(20):
#         t = threading.Thread(target=func, args=(i,))
#         t.start()

#事件 event
#主要用于主线程控制其他线程的执行 (set,wait,clear)

# def do(event):
#     print ('start')
#     event.wait()
#     print ('execute')
#
# event_obj = threading.Event()
#
# event_obj.clear()
#
# for i in range(10):
#     t = threading.Thread(target=do,args=(event_obj,))
#     t.start()
#
# inp = input("input...")
# if inp == 'true':
#     event_obj.set()


#条件
# def run(n):
#     con.acquire()
#     con.wait()
#     print ("run the thread:%s"%n)
#     con.release()
#
# if __name__ == "__main__":
#     con = threading.Condition()
#     for i in range(10):
#         t = threading.Thread(target=run,args=(i,))
#         t.start()
#
#     while True:
#         inp = input(">>>>>>>>")
#         if inp == 'q':
#             break
#         con.acquire()
#         con.notify(int(inp))
#         con.release()


# def condition_func():
#
#     ret = False
#     inp = input('>>>')
#     if inp == '1':
#         ret = True
#     return ret
#
# def run(n):
#     con.acquire()
#     con.wait_for(condition_func)
#     print ("run the thread:%s"%n)
#     con.release()
#
#
# if __name__ == "__main__":
#     con = threading.Condition()
#     for i in range(10):
#         t = threading.Thread(target=run,args=(i,))
#         t.start()

#定时器
# from threading import Timer
#
# def hello():
#     print("hello,world")
#
# t = Timer(8,hello)
# t.start()


# from multiprocessing import Process,Queue
#
# li = []
# def foo(i,q):
#     li.append(i)
#     print ('say hi',i,q.get())
#
# if __name__ == "__main__":
#
#     q = Queue()
#     q.put("h1")
#     q.put("h2")
#     q.put("h3")
#
#     for i in range(10):
#         p = Process(target=foo,args=(i,q))
#         p.start()
#
#     print ('ending',li)

# from multiprocessing import Process, Array,RLock
#
#
# def Foo(lock,temp,i):
#     lock.acquire()
#     temp[0] = 100 + i
#     for item in temp:
#         print(i, '--------->',item)
#     lock.release()
#
#
# if __name__ == "__main__":
#
#     lock = RLock()
#
#     temp = Array('i',[11,22,33,44])
#
#     for i in range(20):
#         p = Process(target=Foo,args=(lock,temp,i))
#         p.start()

# from greenlet import greenlet
#
# def test():
#     print ("12")
#     gr2.switch()
#     print ("34")
#     gr2.switch()
#
# def test2():
#     print ("56")
#     gr1.switch()
#     print ("78")
#
# gr1 = greenlet(test)
# gr2 = greenlet(test2)
# gr1.switch()


#高性能框架 配合协程
import gevent
# def foo():
#     print ("Running in foo")
#     gevent.sleep(0)
#     print ('Explicit context switch to foo again')
#
# def bar():
#     print ("Explicit context to bar")
#     gevent.sleep(0)
#     print('Implicit context switch back to bar')
#
# gevent.joinall([
#     gevent.spawn(foo),
#     gevent.spawn(bar),
# ])

# from gevent import monkey
# monkey.patch_all()
# def eat():
#     print (threading.current_thread().getName())
#     print ("eat food 1")
#     time.sleep(20)
#     print ("eat food 2")
#
# def play():
#     print(threading.current_thread().getName())
#     print("play 1")
#     time.sleep(20)
#     print("play 2")
#
# g1 = gevent.spawn(eat)
# g2 = gevent.spawn(play)
#
# gevent.joinall([
#     g1,g2
# ])

print ("主")

# def judge_lock(fun):
#     def handle(*args,**kwargs):
#
#         print ("damowang------")
#
#         fun(*args,**kwargs)
#         # if 0:
#         #     return
#     return handle
#
# @judge_lock
# def fun():
#     print("777777777777")
#     return 1
# import time
# def decorate(func):
#     def wrapper(*args,**kwargs):
#         start_time = time.time()
#         print ("开始时间",start_time)
#         func(*args,**kwargs)
#         end_time = time.time()
#         print("结束时间", end_time)
#         time_s = end_time - start_time
#         print ("result_time",time_s)
#     return wrapper
#
# @decorate
# def wangkeke():
#     print("ttt---------------")
#
# wangkeke()

# dict = {}
#
# dict.setdefault(1,{})[2] = (8,9)
#
# print ("keke:",dict)

# import  copy
# list_2 = [1,3,5,7]
# new_list_2 = copy.copy(list_2) #仅仅拷贝数据集合的第一层数据
# new_list_3 = copy.deepcopy(list_2) #拷贝数据集合的所有层
#
# new_list_3[2] = 99
# new_list_2[2] = 100
#
#
# print ("keke000->",list_2)
# print ("keke111->",new_list_2)
# print ("keke222->",new_list_3)
#
#
#
#
# n1 = {'k1':'wu','k2':123,'k3':['alex,678']}
#
# print("111---",n1)
# n2 = n1
# print("222---",n2)
#
# n3 = copy.copy(n1)
#
# n4 = copy.deepcopy(n1)
#
# n3['k3'][0] = 'keke'
# # print("333---",(n3))
# print ("333111",n3)
#
# print("111---",n1)
# print("222---",n2)
# print("444---",n4)

# v = dict.fromkeys(["k1","k2"],[])
#
# print ("lllllllll---",v)
# v["k2"].append(666)
#
# print ("22222---",v)
#
# v["k1"]= 777
# print ("3333---",v)
#
# l_dict = {'k1': [], 'k2': []}

# def num():
#     return [lambda x: i*x for i in range(4)]
#
# # print ([m(2) for m in num()])
#
# for m in num():
#
#     print (m)

# t  = (i % 2 for i in range(10))
# b = range(10)
# print (b)
# print (t)

# print (1 or 2)
#
# print (1 == True)

# print (1<2==1)

l_list = "1,2,3"
new_list = l_list.split(",")
print (new_list)
# z = map(int,new_list)
# print (z)

b = [int(x) for x in new_list]
print (b)

# [1,4,9,16,25,36,49,64,81,100]

s = [x*x for x in range(1,11)]
print (s)

s = [11,22,55,55,36,99,88,99]
d = [22,88]

m  = list(set(s)-set(d))

print (m)

# global num

# #二分法
# list_k = [55,8,6,2,14,9,3,2,555,230,4]
# new_list = sorted(list_k)
#
# def fun2fen(new_list,aim_num):
#     middle_num = int(len(new_list) / 2)
#     if len(new_list) > 1:
#         if new_list[middle_num] == aim_num:
#             print("找到了1")
#         elif new_list[middle_num] > aim_num:
#             fun2fen(new_list[0:middle_num],aim_num)
#         else:
#             fun2fen(new_list[middle_num +1:],aim_num)
#
#     else:
#         if new_list[0] == aim_num:
#             print ("找到了")
#         else:
#             print("没找到")
#
#
#
# fun2fen(new_list,1)

import os          #os模块负责程序与操作系统的交互，提供了访问操作系统底层的接口
import sys         #sys模块负责程序与python解释器的交互，提供一系列的函数和变量，用于操控python的运行环境
import random
# print (sys.argv)

print (random.random())
print (random.randint(1,5))
print (random.choice([1,2,3]))


#面向对象

"""
封装---> 将一系列的事物的属性和行为抽象成一个类
继承---> 将一类事物共有的属性和行为抽象成父类，每一个子类都是一个特殊的父类，有父类的行为和属性，也有自己特有的行为和属性
多态--> 
"""

# class aaa():
#     def __init__(self):
#         self.is_open = 1
#         self.name = "aaa"
#
# class aaa2():
#     def __init__(self):
#         self.is_open = 0
#         self.name = "aaa2"
#
# class aaa3():
#     def __init__(self):
#         self.is_open = 1
#         self.name = "aaa3"
#
# class aaa4():
#     def __init__(self):
#         self.is_open = 1
#         self.name = "aaa4"
#
# list = []
# list.append(aaa())
# list.append(aaa2())
# list.append(aaa3())
# list.append(aaa4())
#
# print (list)
# for i in list :
#     print (i.name)
# print ("---------------------------------------")
# new_list = sorted(list,key = lambda x: x.is_open, reverse = True)
#
# for j in new_list:
#     print (j.name)

# def fun(x,*args,**kwargs):
#     print ("1111:",x)
#     print ("111122:", args)
#     print ("111133:", kwargs)
#     return
#
# def fun2(**kwargs):
#     print ("11144",kwargs)
#
#
# # fun(1,2,{1,2},**{1:2})
#
# t1 = {1:2}
# # fun2(k1=t1)
# fun2( **t1)

def decorate(fun):
    def handle_walker(*args,**kwargs):
        if 1:
            print ("keke_do_decorate")
            print ("dd:",args,kwargs)
        fun(*args,**kwargs)


    return handle_walker

@decorate
def fun1(a= 1,b =2):
    print ("装备")

# fun1(9,{"1":2})
def fun4(a):
    try:
        if int(a):
            print ("1111")
    except Exception:
        print ("error!!")

fun4("str")

def fun5(b):
    print ("函数fun5")
    # assert (b==3)
    print ("执行断言")

fun5(4)


HANGING_DATA = {
	1:{
		1:["主线任务",'一直杀,杀到打不过为止','mainline_task','MainLineWaiGua'],
	},

	2:{

	},

	3:{

	},


	4:{
		1: ['环任务', '手动领，每轮做完100次需重新领', 'loop_task','HuanTaskWaiGua'],
		2: ['御前追捕', '三人队伍或者以上，全员无暂离自动开始', 'hunt_task','YuQianWaiGua'],
		3: ['师门任务', '每天20次，不会选择颜色', 'master_task','MasterTaskWaiGua'],
		4: ['宝藏妖怪', '三人队伍或者以上，全员无暂离自动开始', 'monster_task','MonsterTaskWaiGua'],
		5: ['帮派委托', '帮派委托', 'consign_task','BangPaiWaiGua'],
		6: ['杀星', '杀星', 'killstar_task','KillStarWaiGua'],
		7: ['挖宝图', '普通和妖龙，买好了放包裹才会给你挖', 'baotu_task','BaoTuWaiGua'],
		8: ['屏蔽npc', '快捷键alt+n', 'shield_role','ShieldWaiGua'],
		9: ['副本', '副本', 'fuben_task','FuBenWaiGua'],
		10: ['皇家狩猎', '活动时间内才会生效', 'royal_hunting','RoyalHuntWaiGua'],
		11: ['缥缈幻境', '活动时间内才会生效', 'secret_task','SecretTaskWaiGua'],
		12: ['今日卦象', '活动时间内才会生效', 'guaxiang_task','GuaXiangWaiGua'],
	},

}


kp = HANGING_DATA.values()

print (kp)