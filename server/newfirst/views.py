import json
import time
import os
import subprocess
import random

from django.http import HttpResponse, JsonResponse
from newfirst.models import Item, Personnel, DesignCriteria, AnalysisRules, Scenes, Rules, Case, Fmea, Demand, \
    DesignCheck, Design, DesignComplete
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


# 添加单个分析规则
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


# 从项目添加分析规则
def add_analysis_rule_from_item(request):
    request_json = json.loads(request.body)
    try:
        print(request_json)
        # new_name = request_json['name']
        # new_type = request_json['type']
        # new_describe = request_json['describe']
        # new_remark = request_json['remark']
        # if AnalysisRules.objects.filter(name=new_name):
        #     return JsonResponse({**error_code.CLACK_NAME_EXISTS})
        # new_rule = AnalysisRules(name=new_name, type=new_type, remark=new_remark, describe=new_describe)
        # new_rule.save()
        for i in range(len(request_json)):
            blong = request_json[i]['belong']
            if blong == '通用':
                continue
            new_name = request_json[i]['name']
            new_type = request_json[i]['type']
            new_describe = request_json[i]['describe']
            new_remark = request_json[i]['remark']
            if AnalysisRules.objects.filter(name=new_name):
                return JsonResponse({**error_code.CLACK_NAME_EXISTS})
            new_rule = AnalysisRules(name=new_name, type=new_type, remark=new_remark, describe=new_describe)
            new_rule.save()
            Rules.objects.filter(id=request_json[i]['id']).update(belong='通用')
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
        if AnalysisRules.objects.filter(name=new_name).exists():
            return JsonResponse({**error_code.CLACK_NAME_EXISTS})
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
        new_element = request_json['element']
        new_rule = DesignCriteria(type=new_type, describe=new_describe, element=new_element)
        new_rule.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 编辑设计准则
def edit_design_criteria(request):
    request_json = json.loads(request.body)
    try:
        new_describe = request_json['describe']
        aim_id = request_json['id']
        new_name = request_json['name']
        new_type = request_json['type']
        new_element = request_json['element']
        if not DesignCriteria.objects.filter(id=aim_id).exists():
            return JsonResponse({**error_code.CLACK_NOT_EXISTS})
        DesignCriteria.objects.filter(id=aim_id).update(type=new_type)
        DesignCriteria.objects.filter(id=aim_id).update(describe=new_describe)
        DesignCriteria.objects.filter(id=aim_id).update(element=new_element)
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
        new_software = request_json['software']
        new_team = request_json['team']
        new_level = request_json['level']
        new_path = request_json['path']

        if Item.objects.filter(name=new_name):
            return JsonResponse({**error_code.CLACK_NAME_EXISTS})
        new_item = Item(name=new_name,
                        software=new_software,
                        team=new_team,
                        level=new_level,
                        path=new_path)
        new_item.save()
        print(new_item.to_dict())
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "item": new_item.to_dict()})


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
        aim_id = request_json['id']
        Item.objects.get(id=aim_id).delete()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 场景列表
def scenes_list(request):
    request_json = json.loads(request.body)
    try:
        scenes = Scenes.objects.filter(item_id=request_json['id'])
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
        aim_item_id = request_json['item_id']
        if Scenes.objects.filter(name=new_name).exists():
            return JsonResponse({**error_code.CLACK_NAME_EXISTS})
        new_scene = Scenes(name=new_name, describe=new_describe, content=new_content,
                           type=new_type, element=new_element, item_id=aim_item_id)
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
        new_item_id = request_json['item']['id']
        for i in range(len(rule_list)):
            new_name = rule_list[i]['name']
            new_describe = rule_list[i]['describe']
            new_remark = rule_list[i]['remark']
            new_type = rule_list[i]['type']
            new_belong = request_json['belong']
            new_rule = Rules(name=new_name, describe=new_describe, remark=new_remark, type=new_type,
                             item_id=new_item_id, belong=new_belong)
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
        new_rule_id = request_json['rule']['id']
        delete_id_list = request_json['deleteData']
        count = {}
        for i in range(len(request_json['caseData'])):
            case = request_json['caseData'][i]
            if 'name' not in case:
                return JsonResponse({**error_code.CLACK_NULL_ERROR})
            if 'describe' not in case:
                return JsonResponse({**error_code.CLACK_NULL_ERROR})
            if 'content' not in case:
                return JsonResponse({**error_code.CLACK_NULL_ERROR})
            new_content = case['content']
            aim_id = case['id']
            if new_content in count:
                return JsonResponse({**error_code.CLACK_REPEAT_CONTENT})
            else:
                count[new_content] = 0
            if not Case.objects.filter(id=aim_id).exists():
                if Case.objects.filter(rule_id=new_rule_id, case_content=new_content):
                    return JsonResponse({**error_code.CLACK_NAME_EXISTS})
        for i in delete_id_list:
            Case.objects.get(id=i).delete()
        for i in range(len(request_json['caseData'])):
            case = request_json['caseData'][i]
            aim_id = case['id']
            new_name = case['name']
            new_describe = case['describe']
            new_element = case['element']
            new_content = case['content']
            if Case.objects.filter(id=aim_id).exists():
                Case.objects.filter(id=aim_id).update(case_name=new_name)
                Case.objects.filter(id=aim_id).update(case_element=new_element)
                Case.objects.filter(id=aim_id).update(case_content=new_content)
                Case.objects.filter(id=aim_id).update(case_describe=new_describe)
            else:
                new_case = Case(case_name=new_name, case_describe=new_describe, case_content=new_content,
                                case_element=new_element, rule_id=new_rule_id)
                new_case.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 所有规则的实例列表
def case_list(request):
    request_json = json.loads(request.body)
    try:
        aim_item_id = request_json
        case = Case.objects.filter(rule__item=aim_item_id)
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
            res = "unverified"
            if a == 0:
                res = "safe"
            elif a == 1:
                res = "danger"
            Case.objects.filter(id=aim_id).update(verify_result=res)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# fmea失效分析表
def fmea_list(request):
    request_json = json.loads(request.body)
    try:
        aim_item_id = request_json['id']
        cases = Case.objects.filter(verify_result='danger', rule__item=aim_item_id)
        for c in cases:
            if not Fmea.objects.filter(case=c).exists():
                new_fmea = Fmea(case=c)
                new_fmea.save()
        fmeas = Fmea.objects.filter(case__in=cases)
        result = [f.to_dict() for f in fmeas]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "fmea_list": result})


# 编辑fmea
def edit_fmea(request):
    request_json = json.loads(request.body)
    try:
        aim_id = request_json['id']
        new_case_id = request_json['case']
        new_improve = request_json['improve']
        new_influence_level = request_json['influence_level']
        new_local_influence = request_json['local_influence']
        new_reason = request_json['reason']
        new_system_influence = request_json['system_influence']
        new_upper_influence = request_json['upper_influence']
        if not Fmea.objects.filter(id=aim_id).exists():
            return JsonResponse({**error_code.CLACK_NOT_EXISTS})
        Fmea.objects.filter(id=aim_id).update(case_id=new_case_id)
        Fmea.objects.filter(id=aim_id).update(improve=new_improve)
        Fmea.objects.filter(id=aim_id).update(reason=new_reason)
        Fmea.objects.filter(id=aim_id).update(local_influence=new_local_influence)
        Fmea.objects.filter(id=aim_id).update(upper_influence=new_upper_influence)
        Fmea.objects.filter(id=aim_id).update(system_influence=new_system_influence)
        Fmea.objects.filter(id=aim_id).update(influence_level=new_influence_level)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 需求表
def demand_list(request):
    request_json = json.loads(request.body)
    try:
        Fmeas = Fmea.objects.filter(case__rule__item_id=request_json['id'])
        for f in Fmeas:
            if not Demand.objects.filter(fmea=f).exists():
                new_demand = Demand(fmea=f)
                new_demand.save()
        demands = Demand.objects.filter(fmea__in=Fmeas)
        result = [d.to_dict() for d in demands]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "demand_list": result})


# 编辑需求表
def edit_demand(request):
    request_json = json.loads(request.body)
    try:
        aim_id = request_json['id']
        new_fmea_id = request_json['fmea']
        new_demand = request_json['demand']
        if not Demand.objects.filter(id=aim_id).exists():
            return JsonResponse({**error_code.CLACK_NOT_EXISTS})
        Demand.objects.filter(id=aim_id).update(fmea_id=new_fmea_id)
        Demand.objects.filter(id=aim_id).update(demand=new_demand)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 添加规则集
def add_design(request):
    request_json = json.loads(request.body)
    try:
        print(request_json)
        design_list = request_json['selectData']
        new_item_id = request_json['item']['id']
        for i in range(len(design_list)):
            new_name = design_list[i]['name']
            new_describe = design_list[i]['describe']
            new_element = design_list[i]['element']
            new_type = design_list[i]['type']
            if Design.objects.filter(describe=new_describe, type=new_type, element=new_element).exists():
                return JsonResponse({**error_code.CLACK_NAME_EXISTS})
            new_design = Design(name=new_name, describe=new_describe, element=new_element, type=new_type,
                                item_id=new_item_id)
            new_design.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 规则集列表
def designs_list(request):
    request_json = json.loads(request.body)
    try:
        # print(request_json)
        aim_item_id = request_json
        designs = Design.objects.filter(item_id=aim_item_id)
        # rules = Rules.objects.all()
        result = [d.to_dict() for d in designs]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "designs_list": result})


# 删除规则集的中规则
def delete_design(request):
    request_json = json.loads(request.body)
    try:
        # print(request_json)
        for i in range(len(request_json)):
            aim_id = request_json[i]['id']
            if not Design.objects.filter(id=aim_id).exists():
                return JsonResponse({**error_code.CLACK_NOT_EXISTS})
            Design.objects.get(id=aim_id).delete()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 设计核查
def check_list(request):
    request_json = json.loads(request.body)
    try:
        designs = Design.objects.filter(item_id=request_json['id'])
        for d in designs:
            if not DesignCheck.objects.filter(design=d).exists():
                new_design = DesignCheck(design=d)
                new_design.save()
        designCheck = DesignCheck.objects.filter(design__in=designs)
        result = [d.to_dict() for d in designCheck]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "check_list": result})


# 编辑设计核查
def edit_check(request):
    request_json = json.loads(request.body)
    try:
        aim_id = request_json['id']
        new_design_id = request_json['design']
        new_problem = request_json['problem']
        new_suitable = request_json['suitable']
        new_apply = request_json['apply']
        if not DesignCheck.objects.filter(id=aim_id).exists():
            return JsonResponse({**error_code.CLACK_NOT_EXISTS})
        DesignCheck.objects.filter(id=aim_id).update(design_id=new_design_id)
        DesignCheck.objects.filter(id=aim_id).update(apply=new_apply)
        DesignCheck.objects.filter(id=aim_id).update(suitable=new_suitable)
        DesignCheck.objects.filter(id=aim_id).update(problem=new_problem)
        if DesignComplete.objects.filter(designCheck_id=aim_id).exists():
            DesignComplete.objects.get(designCheck_id=aim_id).delete()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 设计完善
def complete_list(request):
    request_json = json.loads(request.body)
    try:
        checks = DesignCheck.objects.filter(apply='适用', suitable='不符合', design__item_id=request_json['id'])
        for c in checks:
            if not DesignComplete.objects.filter(designCheck=c).exists():
                new_complete = DesignComplete(designCheck=c)
                new_complete.save()
        designCompletes = DesignComplete.objects.filter(designCheck__in=checks)
        result = [d.to_dict() for d in designCompletes]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "complete_list": result})


# 编辑设计完善
def edit_complete(request):
    request_json = json.loads(request.body)
    try:
        aim_id = request_json['id']
        new_check_id = request_json['check']
        new_complete = request_json['complete']
        if not DesignComplete.objects.filter(id=aim_id).exists():
            return JsonResponse({**error_code.CLACK_NOT_EXISTS})
        DesignComplete.objects.filter(id=aim_id).update(designCheck_id=new_check_id)
        DesignComplete.objects.filter(id=aim_id).update(complete=new_complete)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})
