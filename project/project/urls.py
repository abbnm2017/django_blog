"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin



from User.views import index

from django.conf import settings
from django.conf.urls.static import static

import notifications.urls




urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^index/', index, name='index'),
    url(r'^user/', include('User.urls', namespace='User')),
    # url(r'^$', include('User.urls', namespace='User')),
    # url(r'', include('User.urls', namespace='User')),
    url(r'^app01/',include('app01.urls',namespace='app01')),

    url(r'^normal/',include('normal.urls',namespace='normal')),

    url(r'^comment/',include('comment.urls',namespace='comment')),

    url(r'^password-reset/',include('password_reset.urls')),

    url(r'inbox/notifications/',include(notifications.urls, namespace='notifications')),

    url(r'notice/',include('notice.urls',namespace='notice')),

    url(r'^$', index, name='index'),

]

#加了这个, 我能访问 http://127.0.0.1:8000/media/article/20210208/85095AB7-8852-468D-9C9E-A19BA6EB2DBC.png

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)