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

from newfirst import views

urlpatterns = [
    path('item_list', views.item_list, name='item_list'),  # 项目列表
    path('design_criteria_list', views.design_criteria_list, name='design_criteria_list'),  # 设计准则列表
    path('analysis_rule_list', views.analysis_rule_list, name='analysis_rule_list'),  # 分析规则列表
    path('add_analysis_rule', views.add_analysis_rule, name='add_analysis_rule'),  # 添加分析规则
    path('add_analysis_rule_from_item', views.add_analysis_rule_from_item, name='add_analysis_rule_from_item'),
    path('edit_analysis_rule', views.edit_analysis_rule, name='edit_analysis_rule'),  # 编辑分析规则
    path('delete_analysis_rule', views.delete_analysis_rule, name='delete_analysis_rule'),  # 删除分析规则
    path('add_design_criteria', views.add_design_criteria, name='add_design_criteria'),  # 添加设计准则
    path('add_design_criteria_from_item', views.add_design_criteria_from_item, name='add_design_criteria_from_item'),
    path('edit_design_criteria', views.edit_design_criteria, name='edit_design_criteria'),  # 编辑设计准则
    path('delete_design_criteria', views.delete_design_criteria, name='delete_design_criteria'),  # 删除设计准则
    path('add_item', views.add_item, name='add_item'),  # 添加项目
    path('edit_item', views.edit_item, name='edit_item'),  # 编辑项目
    path('delete_item', views.delete_item, name='delete_item'),  # 删除项目
    path('scenes_list', views.scenes_list, name='scenes_list'),  # 场景列表
    path('add_scenes', views.add_scenes, name='add_scenes'),  # 添加场景
    path('edit_scenes', views.edit_scenes, name='edit_scenes'),  # 编辑场景
    path('delete_scenes', views.delete_scenes, name='delete_scenes'),  # 删除场景
    path('add_rule', views.add_rule, name='add_rule'),  # 添加规则
    path('rules_list', views.rules_list, name='rules_list'),  # 规则集列表
    path('delete_rule', views.delete_rule, name='delete_rule'),  # 删除规则
    path('add_case_list', views.add_case_list, name='add_case_list'),  # 添加实例列表
    path('add_case', views.add_case, name='add_case'),  # 添加实例
    path('case_list', views.case_list, name='case_list'),  # 添加实例列表
    path('delete_case', views.delete_case, name='delete_case'),  # 删除实例
    path('verify_case', views.verify_case, name='verify_case'),  # 验证实例
    path('verify_case_test', views.verify_case_test, name='verify_case_test'),  # 预检验
    path('reset_case', views.reset_case, name='reset_case'),  # 重置实例
    path('fmea_list', views.fmea_list, name='fmea_list'),  # fmea列表
    path('edit_fmea', views.edit_fmea, name='edit_fmea'),  # 编辑fmea
    path('demand_list', views.demand_list, name='demand_list'),  # 需求表
    path('edit_demand', views.edit_demand, name='edit_demand'),  # 编辑需求表
    path('add_design', views.add_design, name='add_design'),  # 添加准则库
    path('designs_list', views.designs_list, name='designs_list'),  # 规则集列表
    path('delete_design', views.delete_design, name='delete_design'),  # 删除规则
    path('check_list', views.check_list, name='check_list'),  # 设计核查
    path('edit_check', views.edit_check, name='edit_check'),  # 编辑设计核查
    path('complete_list', views.complete_list, name='complete_list'),  # 设计完善
    path('edit_complete', views.edit_complete, name='edit_complete'),  # 编辑设计完善
    path('upload_file', views.upload_file, name='upload_file'),  # 上传文件
    path('import_scenes', views.import_scenes, name='import_scenes'),  # 导入场景
    path('scenes_modeling', views.scenes_modeling, name='scenes_modeling'),  # 场景建模
    path('deliver_model_data', views.deliver_model_data, name='deliver_model_data'),  # 传递模型的场景信息
    path('model_list', views.model_list, name='model_list'),  # 模型列表

]
