"""
author：keke
datetime:2020.1.4.15:44
desc: 中间件
"""
from django.utils.deprecation import MiddlewareMixin
class Middle1(MiddlewareMixin):
    def process_request(self,request):
        print ("m1.process.request")

        #不要给返回值


    def process_response(self, request, response):
        print("m1.process.response")
        return response           #必须要返回结果

    def process_view(self, request, callback, callback_args, callback_kwargs):
       print("m1.process_view")

       print(callback, callback_args, callback_kwargs)
       print("m1.process_view1111")
       response = callback(request, *callback_args, **callback_kwargs)
       return response


def judge_gouzao(fun):
    def handle(*args,**kwargs):
        print("执行装饰器函数。。。")
        print ("000011111",*args)
        print("0000111112222", **kwargs)

        ret = fun(*args,**kwargs)
        return ret
    handle()
    return


class Middle2(MiddlewareMixin):
    def process_request(self,request):
        print ("m2.process.request")

        #不要给返回值


    def process_response(self, request, response):
        print("m2.process.response")
        return response           #必须要返回结果


    # @judge_gouzao
    def process_view(self, request, callback, callback_args, callback_kwargs):
        """
        :param request:
        :param callback:    ==========等于view_fun 视图函数
        :param callback_args:   view_fun 视图函数（参数）
        :param callback_kwargs: view_fun 视图函数（参数）
        :return
        """
        print(callback,callback_args,callback_kwargs)
        print("m2.process_view")
        return callback(request,*callback_args,**callback_kwargs)


# def fun_sort():
#     list_a = [15,35,96,85,12]
#     new_list1 = sorted(list_a,key=lambda x:x, reverse=True)
#     print ("keke11",new_list1)
#     new_list2 = filter(lambda x:x != 35,new_list1)
#     print("keke22", new_list2)
#
# fun_sort()

# def judge_decorate(fun):
#     def handel(*args,**kwargs):
#         print ("aaaaaaaa")
#
#         ret = fun(*args,**kwargs)
#         return ret
#
#     handel()
#     return

"""  *args  **kwargs
    
"""

# def func(*args):
#     print ("keke111------>",args)
#     print ("ppp--->",args[2])
#
# func(1,2,[1,2])

# def func(**kwargs):
#     print ("keke111------>",kwargs)
#     # print ("ppp--->",kargs[2])
#
# func(t= 1)

# *args 将参数打包成tuple(元组)
# **kwargs 讲关键字打包成 dict

# def fun(arg,*args,**kwargs):
#     print ("111",arg)
#     print("222", args)
#     print("333", kwargs)
#
# fun(1,4,5,8,9,1,a= 88)

# def test_arg(arg1,arg2,arg3):
#     print('arg1',arg1)
#     print('arg2', arg2)
#     print('arg3', arg3)
#
# arg1 = 'non'
# arg = ('mar',12)
#
# test_arg(arg1,*arg)


# def test_arg(**kwarg):
#     for k,v in kwarg.items():
#         print ("k---->v",k,v)

# test_arg(a= "name",b = "sex")


arg={'arg1':'name','arg2':"sex",'arg3':52}
#
# def test_arg(arg1,arg2,arg3):
#     print("arg1",arg1)
#     print("arg2", arg2)
#     print("arg3", arg3)
#
# test_arg(**arg)


from threading import Timer

def func(ars):
    # print ("keke--科科大魔王",ars)
    return

s = Timer(2,func,(1,))
s.start()
