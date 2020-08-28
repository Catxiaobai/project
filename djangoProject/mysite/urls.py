"""djangoProject URL Configuration

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
from mysite import views

urlpatterns = [
    url(r'^modeling', views.modeling, name='modeling'),  # 生成模型
    url(r'^showModel', views.showModel, name='showModel'),  # 展示模型
    url(r'^judgeModel', views.judgeModel, name='judgeModle'),  # 完整性检验
    url(r'^addModel', views.addModel, name='addModel'),  # 模型补全
    url(r'^safeVerify', views.safeVerify, name='safeVerify'),  # 安全性验证

]
