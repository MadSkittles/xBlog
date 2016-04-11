"""MyBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve
from xBlog.views import *
from . import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    url(r'^tag/(?P<tag_name>[\w-]+)/$', get_tag_list, name='tags'),
    url(r'^archive/(?P<archive_name>[\w-]+)/$', get_archive_list, name='archives'),
    url(r'^catagory/(?P<catagory_name>[\w-]+)/$', get_catagory_list, name='catagories'),
    url(r'^article/(?P<article_id>\d+)/$', get_detail, name='detail'),
    url(r'^alipay$', alipay, name='alipay'),
    url(r'^comment/(?P<article_id>\d+)/$', submit_comment),
    url(r'^today-visitors/$', today_visitors),
    url(r'^online-visitors/$', online_visitors),
    url(r'^resume/$', resume, name='resume'),
]

if settings.DEBUG is False:

    urlpatterns += [url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})]
else:
    urlpatterns += [url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_URL})]
