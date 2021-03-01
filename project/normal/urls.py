from django.conf.urls import url

from . import views\

from django.views import View

app_name = 'normal'

urlpatterns = [
    url('^login/',views.user_login,name='login'),
    url('^logout/',views.user_loginout,name='logout'),
    url('^register/',views.user_register,name='register'),
    url('^delete/(\d+)',views.user_delete,name='user_delete'),

]
