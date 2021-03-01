from django.conf.urls import url

from . import views
app_name = 'comment'

urlpatterns = [

    url('^post_comment/(\d+)$', views.comment, name='post_comment'),
    url('^post_comment/(\d+)/(\d+)', views.comment, name='comment_reply'),

    url('^home/', views.home, name='home'),
    url('^send/message/', views.send_message, name='send_message'),
    url('^get/message/', views.get_message, name='get_message'),
]