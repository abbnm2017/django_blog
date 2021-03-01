from django.conf.urls import url
from . import views

from User.newviews import account
from User.newviews import love
# from User.views import *
app_name = 'User'

urlpatterns = [
    url(r'nginx.html', views.nginx2, name = "nginx2"),
    url(r'add_teachers/', views.add_teachers, name='add_teachers'),
    url(r'modal_addstudent/',views.modal_addstudent, name = 'modal_addstudent'),
    url(r'^$', views.index, name="index"),
    url(r'chatlogin/', views.chatlogin, name = "chatlogin"),
    url(r'chatlogout/', views.chatlogout, name = "chatlogout"),
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

    url(r'tcp_socket/', views.tcp_socket, name="tcp_socket"),
    url(r'floatpic/', views.floatpic, name = 'floatpic'),
    
    url(r'uploadImg/', views.uploadImg, name = "uploadImg"),
    
    url(r'showImg/', views.showImg, name = "showImg"),
    
    url(r'reptile/', views.reptile, name = "reptile"),
    
    url(r'chat/', views.chat, name = "chat"),
    
    url(r'conn/', views.conn, name = "conn"),

    url(r'^$', views.classes, name="classes"),
    url(r'classes/',views.classes, name = 'classes'),

    url(r'addstudent/',views.addstudent, name = 'addstudent'),

    url(r'edit_student/',views.edit_student, name = 'edit_student'),

    url(r'del_student/',views.del_student, name = 'del_student'),

    url(r'del_student2/',views.del_student2, name = 'del_student2'),

    url(r'modal_addstudent2/',views.modal_addstudent2, name = 'modal_addstudent2'),

    url(r'newstudent/',views.newstudent, name = 'newstudent'),
    url(r'modal_add_student/',views.modal_add_student, name = 'modal_add_student'),
    url(r'update_add_student/',views.update_add_student, name = 'update_add_student'),
    url(r'^teachers/',views.teachers, name = 'teachers'),
    url(r'^edit_teacher/',views.edit_teacher, name = 'edit_teacher'),

    url(r'^newadd_teacher/',views.newadd_teacher, name = 'newadd_teacher'),
    url(r'^layout/',views.layout, name = 'layout'),

    url(r'^del_student_nowlist/',views.del_student_nowlist, name='del_student_nowlist'),
    url(r'^edit_student_list/',views.edit_student_list, name='edit_student_list'),
    url(r'^del_teacher_info/',views.del_teacher_info, name='del_teacher_info'),
    url(r'^test_fenye/',views.test_fenye, name='test_fenye'),

    url(r'^custom/',views.custom,name='custom'),

    url(r'^csrf.html$',views.csrf,name='csrf'),

    url(r'^marrylogin.html$',account.login,name='account_login'),
    url(r'^marryindex.html$', love.index, name='love_index'),
    url(r'^marrylogout.html$', account.logout, name='account_logout'),
    url(r'^marrytest.html$', account.test, name='account_test'),

]