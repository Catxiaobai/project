"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from entity import views

urlpatterns = [
    # path('test', views.test, name='test'),
    path('modeling', views.modeling, name='modeling'),  # 生成模型
    path('show_model', views.show_model, name='show_model'),  # 展示模型
    path('judge_model', views.judge_model, name='judge_model'),  # 完整性检验
    path('add_model', views.add_model, name='add_model'),  # 模型补全
    path('safe_verify', views.safe_verify, name='safe_verify'),  # 安全性验证
    path('trace_list', views.trace_list, name='trace_list'),  # trace列表
]
