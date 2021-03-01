from django.conf.urls import url
from . import views

from User.newviews import account
from User.newviews import love
# from User.views import *
app_name = 'app01'

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^commit/', views.ajax_commit,name='ajax_commit'),
    url(r'^login1/', views.mm_login, name='mm_login'),
    url(r'^class_list/', views.class_list, name='class_list'),
    url(r'^add_class/', views.add_class, name='add_class'),
    url(r'^edit_class/(\d+)/', views.edit_class, name='edit_class'),

    url(r'^student_list/', views.student_list, name='student_list'),
    url(r'^add_student/', views.add_student, name='add_student'),
    url(r'^edit_student/(\d+)', views.edit_student, name='edit_student'),

    url(r'^teacher_list/', views.teacher_list, name='teacher_list'),
    url(r'^add_teacher/', views.add_teacher, name='add_teacher'),
    url(r'^edit_teacher/(\d+)', views.edit_teacher, name='edit_teacher'),

    url(r'^new_ajax/',views.new_ajax,name="new_ajax"),
    url(r'^add1/',views.add1,name="add1"),
    url(r'^add2/',views.add2,name="add2"),
    url(r'^autohome/',views.autohome,name="autohome"),
    url(r'^fake_ajax/',views.fake_ajax,name="fake_ajax"),
    url(r'^upload/',views.upload,name="upload"),
    url(r'^yuan_ajax/$',views.yuan_ajax,name="yuan_ajax"),
    url(r'^jsonp/$',views.jsonp,name="jsonp"),
    url(r'^article/$',views.article,name="article"),
    url(r'^article_detail/(\d+)/',views.article_detail,name="article_detail"),
    url(r'^article_create/',views.article_create,name="article_create"),
    url(r'^article_delete/(\d+)/$',views.article_delete,name="article_delete"),
    url(r'^article_update/(\d+)/$',views.article_update,name="article_update"),

    url(r'^test/',views.ArticleListView.as_view(), name='test-view'),

    url(r'^increase_likes/(\d+)/',views.IncreaseLikesView.as_view(), name='increase-likes'),



]