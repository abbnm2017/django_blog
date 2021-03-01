from django.shortcuts import render,HttpResponse,redirect
from User import models
def index(request):
    if not request.session.get('user_info'):
        print ("ke112222222222222222233333333333")
        return redirect('marrylogin.html')
    else:
        #男生，查看女生列表
        #女生,查看男生列表
        gender = request.session.get('user_info').get('gender')
        if gender == 1:
            user_list = models.MarryBoy.objects.all()
        else:
            user_list = models.MarryGirl.objects.all()
        nickname = request.session.get('user_info').get('nickname')
        print("kekeaaa,",nickname)
        return render(request,'marry/marryindex.html', {'user_list':user_list,'nickname':nickname})