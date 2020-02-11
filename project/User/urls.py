from django.conf.urls import url
from . import views

# from User.views import *
app_name = 'User'

urlpatterns = [
    url(r'^$', views.index, name="index"),
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

]