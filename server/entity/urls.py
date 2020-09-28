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
    path('add_trace', views.add_trace, name='add_trace'),  # 添加trace
    path('delete_trace', views.delete_trace, name='delete_trace'),  # 添加trace
    path('edit_trace', views.edit_trace, name='edit_trace'),  # 编辑trace
    path('import_trace', views.import_trace, name='import_trace'),  # trace列表
    path('invalid_list', views.invalid_list, name='invalid_list'),  # trace列表
    path('add_invalid', views.add_invalid, name='add_invalid'),  # 添加trace
    path('delete_invalid', views.delete_invalid, name='delete_invalid'),  # 添加trace
    path('edit_invalid', views.edit_invalid, name='edit_invalid'),  # 编辑trace
    path('import_invalid', views.import_invalid, name='import_invalid'),  # 导入trace
    path('verify_invalid', views.verify_invalid, name='verify_invalid'),  # 安全性验证
    path('reset_verify', views.reset_verify, name='reset_verify'),  # 重置安全性验证信息
    path('deliver_model', views.deliver_model, name='deliver_model'),  # 传递模型数据
    path('verify_add', views.verify_add, name='verify_add_link'),  # 验证对模型的添加操作
    path('verify_del', views.verify_del, name='verify_del_link'),  # 验证对模型的删除操作
]
