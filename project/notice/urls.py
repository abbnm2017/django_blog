from django.conf.urls import url
from . import views

app_name = 'notice'

urlpatterns = [
    url('^list/',views.CommentNoticeListView.as_view(),name='list'),
    url('^update/',views.CommentNoticeUpdateView.as_view(),name='update'),
]
