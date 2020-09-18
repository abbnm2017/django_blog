from django.conf.urls import url
from . import views

# from User.views import *
app_name = 'User'

urlpatterns = [
    url(r'modal_addstudent/',views.modal_addstudent, name = 'modal_addstudent'),
    url(r'^$', views.index, name="index"),
    url(r'chatlogin/', views.chatlogin, name = "chatlogin"),
    url(r'codelogin/', views.code_login, name="codelogin"),
    url(r'^register/', views.user_register, name="register"),
    url(r'fail/', views.failed, name = 'fail'),
    url(r'zhuce/', views.user_zhuce, name='zhuce'),
    url(r'login/',views.user_login, name="login"),
    url(r'logout/', views.user_logout, name="logout"),
    url(r'sendcode/', views.send_code, name="send_code"),
    url(r'about/', views.about, name = "about"),
    url(r'board/', views.board, name = "board"),
    url(r'board_post/', views.board_post, name = "board_post"),
    url(r'lifeopen/', views.life_open, name = "lifeopen"),
    url(r'zanshang/', views.zanshang, name = "zanshang"),
    url(r'need1/', views.need1, name = "need1"),
    url(r'test_ajax/', views.test_ajax, name = "test_ajax"),
    url(r'like_change/', views.like_change, name = "like_change"),
    url(r'need2/', views.need2, name = "need2"),
    url(r'need3/', views.need3, name = "need3"),
    url(r'need4/', views.need4, name = "need4"),
    url(r'need5/', views.need5, name = "need5"),
    url(r'need6/', views.need6, name = "need6"),
    url(r'need7/', views.need7, name = "need7"),

    url(r'loading/', views.loading, name = "loading"),
    url(r'floatpic/', views.floatpic, name = 'floatpic'),

    url(r'uploadImg/', views.uploadImg, name = "uploadImg"),

    url(r'showImg/', views.showImg, name = "showImg"),

    url(r'reptile/', views.reptile, name = "reptile"),

    url(r'chat/', views.chat, name = "chat"),

    url(r'conn/', views.conn, name = "conn"),

    url(r'classes/',views.classes, name = 'classes'),

    url(r'addstudent/',views.addstudent, name = 'addstudent'),

    url(r'edit_student/',views.edit_student, name = 'edit_student'),

    url(r'del_student/',views.del_student, name = 'del_student'),



]