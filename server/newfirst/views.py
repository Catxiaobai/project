import json
import time
import os
import subprocess
import random

from django.http import HttpResponse, JsonResponse
from newfirst.models import Item, Personnel, DesignCriteria, AnalysisRules, Scenes, Rules, Case
from server import error_code
from django.shortcuts import render


# Create your views here.


# 查询全部项目
def item_list(request):
    try:
        items = Item.objects.all()
        result = [item.to_dict() for item in items]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "item_list": result})


# 查询设计准则
def design_criteria_list(request):
    try:
        designs = DesignCriteria.objects.all()
        result = [design.to_dict() for design in designs]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "design_list": result})


# 查询分析规则
def analysis_rule_list(request):
    try:
        analysis = AnalysisRules.objects.all()
        result = [a.to_dict() for a in analysis]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "analysis_list": result})


# 添加分析规则
def add_analysis_rule(request):
    request_json = json.loads(request.body)
    try:
        new_name = request_json['name']
        new_type = request_json['type']
        new_describe = request_json['describe']
        new_remark = request_json['remark']
        if AnalysisRules.objects.filter(name=new_name):
            return JsonResponse({**error_code.CLACK_NAME_EXISTS})
        new_rule = AnalysisRules(name=new_name, type=new_type, remark=new_remark, describe=new_describe)
        new_rule.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 编辑分析规则
def edit_analysis_rule(request):
    request_json = json.loads(request.body)
    try:
        aim_id = request_json['id']
        new_name = request_json['name']
        new_type = request_json['type']
        new_describe = request_json['describe']
        new_remark = request_json['remark']
        if not AnalysisRules.objects.filter(id=aim_id).exists():
            return JsonResponse({**error_code.CLACK_NOT_EXISTS})
        AnalysisRules.objects.filter(id=aim_id).update(name=new_name)
        AnalysisRules.objects.filter(id=aim_id).update(type=new_type)
        AnalysisRules.objects.filter(id=aim_id).update(describe=new_describe)
        AnalysisRules.objects.filter(id=aim_id).update(remark=new_remark)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 删除分析规则
def delete_analysis_rule(request):
    request_json = json.loads(request.body)
    try:
        # print(request_json)
        for i in range(len(request_json)):
            aim_id = request_json[i]['id']
            if not AnalysisRules.objects.filter(id=aim_id).exists():
                return JsonResponse({**error_code.CLACK_NOT_EXISTS})
            AnalysisRules.objects.get(id=aim_id).delete()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 添加设计准则
def add_design_criteria(request):
    request_json = json.loads(request.body)
    try:
        new_name = request_json['name']
        new_type = request_json['type']
        new_describe = request_json['describe']
        new_remark = request_json['remark']
        if DesignCriteria.objects.filter(name=new_name):
            return JsonResponse({**error_code.CLACK_NAME_EXISTS})
        new_rule = DesignCriteria(name=new_name, type=new_type, remark=new_remark, describe=new_describe)
        new_rule.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 编辑设计准则
def edit_design_criteria(request):
    request_json = json.loads(request.body)
    try:
        new_describe = request_json['describe']
        new_remark = request_json['remark']
        aim_id = request_json['id']
        new_name = request_json['name']
        new_type = request_json['type']
        if not DesignCriteria.objects.filter(id=aim_id).exists():
            return JsonResponse({**error_code.CLACK_NOT_EXISTS})
        DesignCriteria.objects.filter(id=aim_id).update(name=new_name)
        DesignCriteria.objects.filter(id=aim_id).update(type=new_type)
        DesignCriteria.objects.filter(id=aim_id).update(describe=new_describe)
        DesignCriteria.objects.filter(id=aim_id).update(remark=new_remark)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 删除设计准则
def delete_design_criteria(request):
    request_json = json.loads(request.body)
    try:
        # print(request_json)
        for i in range(len(request_json)):
            aim_id = request_json[i]['id']
            if not DesignCriteria.objects.filter(id=aim_id).exists():
                return JsonResponse({**error_code.CLACK_NOT_EXISTS})
            DesignCriteria.objects.get(id=aim_id).delete()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 新建项目
def add_item(request):
    request_json = json.loads(request.body)
    try:
        new_name = request_json['name']
        new_introduction = request_json['introduction']
        new_content = 'new_content'
        # new_date = "2020-10-23"
        if Item.objects.filter(item_name=new_name):
            return JsonResponse({**error_code.CLACK_NAME_EXISTS})
        new_item = Item(item_name=new_name, item_introduction=new_introduction,
                        item_content=new_content)
        new_item.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 编辑项目
def edit_item(request):
    request_json = json.loads(request.body)
    try:
        aim_id = request_json['id']
        new_name = request_json['name']
        new_introduction = request_json['introduction']
        if not Item.objects.filter(id=aim_id).exists():
            return JsonResponse({**error_code.CLACK_NOT_EXISTS})
        Item.objects.filter(id=aim_id).update(item_name=new_name)
        Item.objects.filter(id=aim_id).update(item_introduction=new_introduction)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 删除项目
def delete_item(request):
    request_json = json.loads(request.body)
    try:
        aim_id = request_json['item_id']
        Item.objects.get(id=aim_id).delete()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 场景列表
def scenes_list(request):
    try:
        scenes = Scenes.objects.all()
        result = [scene.to_dict() for scene in scenes]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "scenes_list": result})


def add_scenes(request):
    request_json = json.loads(request.body)
    try:
        new_name = request_json['name']
        new_describe = request_json['describe']
        new_content = request_json['content']
        new_type = request_json['type']
        new_element = request_json['element']
        if Scenes.objects.filter(name=new_name):
            return JsonResponse({**error_code.CLACK_NAME_EXISTS})
        new_scene = Scenes(name=new_name, describe=new_describe, content=new_content,
                           type=new_type, element=new_element)
        new_scene.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 编辑场景
def edit_scenes(request):
    request_json = json.loads(request.body)
    try:
        new_describe = request_json['describe']
        new_element = request_json['element']
        new_content = request_json['content']
        aim_id = request_json['id']
        new_name = request_json['name']
        new_type = request_json['type']
        if not Scenes.objects.filter(id=aim_id).exists():
            return Scenes({**error_code.CLACK_NOT_EXISTS})
        Scenes.objects.filter(id=aim_id).update(name=new_name)
        Scenes.objects.filter(id=aim_id).update(type=new_type)
        Scenes.objects.filter(id=aim_id).update(describe=new_describe)
        Scenes.objects.filter(id=aim_id).update(element=new_element)
        Scenes.objects.filter(id=aim_id).update(content=new_content)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 删除场景
def delete_scenes(request):
    request_json = json.loads(request.body)
    try:
        # print(request_json)
        for i in range(len(request_json)):
            aim_id = request_json[i]['id']
            if not Scenes.objects.filter(id=aim_id).exists():
                return JsonResponse({**error_code.CLACK_NOT_EXISTS})
            Scenes.objects.get(id=aim_id).delete()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 添加规则集
def add_rule(request):
    request_json = json.loads(request.body)
    try:
        print(request_json)
        rule_list = request_json['selectData']
        new_item_id = request_json['item']['item_id']
        for i in range(len(rule_list)):
            new_name = rule_list[i]['name']
            new_describe = rule_list[i]['describe']
            new_remark = rule_list[i]['remark']
            new_type = rule_list[i]['type']
            new_rule = Rules(name=new_name, describe=new_describe, remark=new_remark, type=new_type,
                             item_id=new_item_id)
            new_rule.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 规则集列表
def rules_list(request):
    request_json = json.loads(request.body)
    try:
        # print(request_json)
        aim_item_id = request_json
        rules = Rules.objects.filter(item_id=aim_item_id)
        # rules = Rules.objects.all()
        result = [r.to_dict() for r in rules]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "rules_list": result})


# 删除规则集的中规则
def delete_rule(request):
    request_json = json.loads(request.body)
    try:
        # print(request_json)
        for i in range(len(request_json)):
            aim_id = request_json[i]['id']
            if not Rules.objects.filter(id=aim_id).exists():
                return JsonResponse({**error_code.CLACK_NOT_EXISTS})
            Rules.objects.get(id=aim_id).delete()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 所选规则的实例列表
def add_case_list(request):
    request_json = json.loads(request.body)
    try:
        # print(request_json)
        aim_rule_id = request_json
        case = Case.objects.filter(rule_id=aim_rule_id)
        # rules = Rules.objects.all()
        result = [c.to_dict() for c in case]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "case_list": result})


# 添加实例
def add_case(request):
    request_json = json.loads(request.body)
    try:
        print(request_json)
        case = request_json['addData']
        new_rule_id = request_json['rule']['id']
        new_name = case['name']
        new_describe = case['describe']
        new_element = case['element']
        new_content = case['content']
        new_case = Case(case_name=new_name, case_describe=new_describe, case_content=new_content,
                        case_element=new_element,
                        rule_id=new_rule_id)
        new_case.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 所有规则的实例列表
def case_list(request):
    try:
        case = Case.objects.all()
        result = [c.to_dict() for c in case]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "case_list": result})


# 删除实例
def delete_case(request):
    request_json = json.loads(request.body)
    try:
        # print(request_json)
        for i in range(len(request_json)):
            aim_id = request_json[i]['id']
            if not Case.objects.filter(id=aim_id).exists():
                return JsonResponse({**error_code.CLACK_NOT_EXISTS})
            Case.objects.get(id=aim_id).delete()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 重置实例验证结果
def reset_case(request):
    request_json = json.loads(request.body)
    try:
        for i in range(0, len(request_json)):
            aim_id = request_json[i]['id']
            if not Case.objects.filter(id=aim_id).exists():
                return JsonResponse({**error_code.CLACK_NOT_EXISTS})
            Case.objects.filter(id=aim_id).update(verify_result="unverified")
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 验证实例
def verify_case(request):
    request_json = json.loads(request.body)
    # print(request_json)
    try:
        for i in range(0, len(request_json)):
            aim_id = request_json[i]['id']
            if not Case.objects.filter(id=aim_id).exists():
                return JsonResponse({**error_code.CLACK_NOT_EXISTS})
            a = random.randint(0, 1)
            if a == 0:
                res = "safe"
            elif a == 1:
                res = "danger"
            Case.objects.filter(id=aim_id).update(verify_result=res)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})
