"""FileShare URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
# 导入视图函数中的对象
from Share.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$',LoginView.as_view(), name='login'),
    # 引用视图对象需要调用对象的as_view(),因为以对象去调用，所以必须加括号
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^s/(?P<code>\d+)/$', DisplayView.as_view(), name='s'),
    url(r'^my/$', MyView.as_view(), name='my'),
    url(r'^search/', SearchView.as_view(), name='search')
]
