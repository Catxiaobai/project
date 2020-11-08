import json
import time
import os
import subprocess
import random

from django.http import HttpResponse, JsonResponse
from newfirst.models import Item, Personnel, DesignCriteria, AnalysisRules, Scenes, Rules, Case, Fmea, Demand, \
    DesignCheck, Design, DesignComplete
from server import error_code
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
# from lwn_Graphic.constructModel import constructModel
# from lwn_Graphic.combination import combination
import lwn_Graphic.combination
import lwn_Graphic.constructModel
import lwn_Graphic.constructModel2
import lwn_Graphic.combination2
# import lxd_verify.Main
import newVerify.Main


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
        for i in range(len(request_json)):
            belong = request_json[i]['belong']
            if belong == '通用':
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


# 将专用设计准则加入通用设计准则中
def add_design_criteria_from_item(request):
    request_jsons = json.loads(request.body)
    try:
        print(request_jsons)
        for request_json in request_jsons:
            if request_json['belong'] == '通用':
                continue
            new_type = request_json['type']
            new_describe = request_json['describe']
            new_element = request_json['element']
            new_rule = DesignCriteria(type=new_type, describe=new_describe, element=new_element)
            new_rule.save()
            Design.objects.filter(id=request_json['id']).update(belong='通用')
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
        os.makedirs('./'+new_path + '/' + new_name)
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
        # 找当前项目相关的实例
        aim_item_id = request_json
        # 判断规则集是否为空以及是否存在规则未实例化
        info = ""
        left_rules_id = []
        # 判断规则集是否为空
        rules = Rules.objects.filter(item_id=aim_item_id)
        if len(rules) == 0:
            info = "当前项目规则集为空"
        # 判断规则是否实例化
        else:
            for r in rules:
                if len(Case.objects.filter(rule=r)) == 0:
                    left_rules_id.append(r.id)
        # 展示当前项目下的全部实例
        case = Case.objects.filter(rule__item_id=aim_item_id)
        result = [c.to_dict() for c in case]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "case_list": result, "info": info, "left_rules_id": left_rules_id})


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
            res = "未检验"
            # 判断应该使用哪一个方法验证
            aim_element = request_json[i]['element']
            aim_rule_describe = request_json[i]['rule_describe']
            if aim_element == '状态迁移':
                if aim_rule_describe == 'ATM系统的安全性验证':
                    aim_content = request_json[i]['content']
                    print(aim_content)
                    with open('./file/targetInvalid.txt', 'w') as f:  # 设置文件对象
                        f.write('Transition:\n')
                        f.write(aim_content)
                    # os.system('py -2 E:/Code/project301/lxd_Safety/graphTraversal-submit2/execution/project_gui.py')

                    with open('./file/path.txt') as f:
                        lines = f.read()
                    if len(lines) > 2:
                        res = "违背"
                    else:
                        res = "符合"
            else:
                a = random.randint(0, 1)
                if a == 0:
                    res = "符合"
                elif a == 1:
                    res = "违背"
            new_count = Case.objects.get(id=aim_id).verify_count + 1
            last_result = Case.objects.get(id=aim_id).verify_result

            Case.objects.filter(id=aim_id).update(verify_result=res)
            Case.objects.filter(id=aim_id).update(verify_count=new_count)
            Case.objects.filter(id=aim_id).update(last_verify_result=last_result)
            if Case.objects.get(id=aim_id).verify_result == "违背":
                # 加入失效分析
                new_case_name = Case.objects.get(id=aim_id).case_name
                new_case_describe = Case.objects.get(id=aim_id).case_describe
                new_case_element = Case.objects.get(id=aim_id).case_element
                new_case_content = Case.objects.get(id=aim_id).case_content
                new_item_id = Case.objects.get(id=aim_id).rule.item_id
                new_fmea = Fmea(case_content=new_case_content, case_describe=new_case_describe,
                                case_element=new_case_element, case_name=new_case_name, item_id=new_item_id)
                new_fmea.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 预检验
def verify_case_test(request):
    request_json = json.loads(request.body)
    print(request_json)
    try:
        for i in range(0, len(request_json)):
            aim_id = request_json[i]['id']
            if not Case.objects.filter(id=aim_id).exists():
                return JsonResponse({**error_code.CLACK_NOT_EXISTS})
            res = "未检验"
            # 判断应该使用哪一个方法验证
            aim_element = request_json[i]['element']
            aim_rule_describe = request_json[i]['rule_describe']
            if aim_element == '状态迁移':
                if aim_rule_describe == 'ATM系统的安全性验证':
                    aim_content = request_json[i]['content']
                    print(aim_content)
                    with open('./file/targetInvalid.txt', 'w') as f:  # 设置文件对象
                        f.write('Transition:\n')
                        # print(aim_content)
                        ttt = aim_content.split('\n')
                        for t in ttt:
                            # print('\t'+t)
                            f.write('\t' + t + '\n')
                        # f.write(aim_content)
                    # os.system('py -2 E:/Code/project301/lxd_Safety/graphTraversal-submit2/execution/project_gui.py')
                    # lxd_verify.Main.main()
                    # newVerify.Main.main()
                    # with open('./file/path.txt') as f:
                    #     lines = f.read()
                    # if len(lines) > 8:
                    #     res = "违背"
                    # else:
                    #     res = "符合"
                    a = random.randint(0, 1)
                    if a == 0:
                        res = "符合"
                    elif a == 1:
                        res = "违背"
            else:
                a = random.randint(0, 1)
                if a == 0:
                    res = "符合"
                elif a == 1:
                    res = "违背"
            last_result = Case.objects.get(id=aim_id).verify_result
            Case.objects.filter(id=aim_id).update(verify_result=res)
            Case.objects.filter(id=aim_id).update(last_verify_result=last_result)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# fmea失效分析表
def fmea_list(request):
    request_json = json.loads(request.body)
    try:
        aim_item_id = request_json['id']
        fmeas = Fmea.objects.filter(item_id=aim_item_id)
        result = [f.to_dict() for f in fmeas]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "fmea_list": result})


# 编辑fmea
def edit_fmea(request):
    request_jsons = json.loads(request.body)
    try:
        print(request_jsons)
        for request_json in request_jsons:
            aim_id = request_json['id']
            if request_json['ignore']:
                Fmea.objects.filter(id=aim_id).update(ignore=True)
            else:
                new_improve = request_json['improve']
                new_influence_level = request_json['influence_level']
                new_local_influence = request_json['local_influence']
                new_reason = request_json['reason']
                new_system_influence = request_json['system_influence']
                new_upper_influence = request_json['upper_influence']
                new_describe = request_json['describe']
                if not Fmea.objects.filter(id=aim_id).exists():
                    return JsonResponse({**error_code.CLACK_NOT_EXISTS})
                Fmea.objects.filter(id=aim_id).update(improve=new_improve)
                Fmea.objects.filter(id=aim_id).update(reason=new_reason)
                Fmea.objects.filter(id=aim_id).update(local_influence=new_local_influence)
                Fmea.objects.filter(id=aim_id).update(upper_influence=new_upper_influence)
                Fmea.objects.filter(id=aim_id).update(system_influence=new_system_influence)
                Fmea.objects.filter(id=aim_id).update(influence_level=new_influence_level)
                Fmea.objects.filter(id=aim_id).update(describe=new_describe)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 需求表
def demand_list(request):
    request_json = json.loads(request.body)
    try:
        Fmeas = Fmea.objects.filter(item_id=request_json['id'], ignore=False)
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
    request_jsons = json.loads(request.body)
    try:
        print(request_jsons)
        for request_json in request_jsons:
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
        new_belong = request_json['belong']
        for i in range(len(design_list)):
            new_name = design_list[i]['name']
            new_describe = design_list[i]['describe']
            new_element = design_list[i]['element']
            new_type = design_list[i]['type']
            if Design.objects.filter(describe=new_describe, type=new_type, element=new_element).exists():
                return JsonResponse({**error_code.CLACK_NAME_EXISTS})
            new_design = Design(name=new_name, describe=new_describe, element=new_element, type=new_type,
                                item_id=new_item_id, belong=new_belong)
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
    request_jsons = json.loads(request.body)
    try:
        for request_json in request_jsons:
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
    request_jsons = json.loads(request.body)
    try:
        for request_json in request_jsons:
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


# 上传文件
def upload_file(request):
    myfile = request.FILES['file']
    fs = FileSystemStorage(location='file')
    if fs.exists(myfile.name):
        fs.delete(myfile.name)
    fs.save(myfile.name, myfile)
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 从txt文件中导入场景
def import_scenes(request):
    request_json = json.loads(request.body)
    filename = request_json['name']
    new_element = request_json['name'][:-4]
    new_type = request_json['type']
    new_item = request_json['item']
    try:
        with open('./file/' + filename, 'r', encoding='utf-8') as f:
            original_file = f.read()
            lines = original_file.splitlines()
        index = 0
        while index < len(lines):
            if '0' <= lines[index][0] <= '9':
                index += 1
                new_content = ""
                new_name = ""
                new_describe = ""
                if lines[index] == "name:":
                    index += 1
                    new_name = lines[index]
                    index += 1
                if lines[index] == "describe:":
                    index += 1
                    new_describe = lines[index]
                    index += 1
                if lines[index] == "content:":
                    index += 1
                while index < len(lines) and (lines[index][0] <= '0' or lines[index][0] >= '9'):
                    new_content = new_content + lines[index] + '\n'
                    index += 1
                scenes = Scenes(item_id=new_item['id'],
                                element=new_element,
                                content=new_content,
                                type=new_type,
                                name=new_name,
                                describe=new_describe)
                scenes.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 从数据库中导出场景建模
def scenes_modeling(request):
    request_jsons = json.loads(request.body)
    try:
        scenes = Scenes.objects.filter(item_id=request_jsons['item']['id'], type=request_jsons['type'])
        if request_jsons['type'] == 'sub':
            filename = 'Trace.txt'
        elif request_jsons['type'] == 'complex':
            filename = 'Trace2.txt'

        f = open('./file/' + filename, 'w', encoding='utf-8')
        for s in scenes:
            print(s.to_dict())
            ch = s.to_dict()
            f.write('Trace:' + '\n')
            f.write(ch['content'])
        f.close()
        if request_jsons['type'] == 'sub':
            lwn_Graphic.constructModel.main()
            lwn_Graphic.combination.combination()
            filepath = './file/'
            with open(filepath + 'resultSaveCreate.txt', 'wt+', encoding='utf-8') as f:
                f.write(open(filepath + 'result.txt', 'r', encoding='utf-8').read())
            with open(filepath + 'resultModelSaveCreate.txt', 'wt+', encoding='utf-8') as f:
                f.write(open(filepath + 'resultModel.txt', 'r', encoding='utf-8').read())
        elif request_jsons['type'] == 'complex':
            lwn_Graphic.constructModel2.main()
            lwn_Graphic.combination2.combination()
            filepath = './file/'
            with open(filepath + 'resultSaveCreate.txt', 'wt+', encoding='utf-8') as f:
                f.write(open(filepath + 'result2.txt', 'r', encoding='utf-8').read())
            with open(filepath + 'resultModelSaveCreate.txt', 'wt+', encoding='utf-8') as f:
                f.write(open(filepath + 'resultModel2.txt', 'r', encoding='utf-8').read())
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


def deliver_model_data(request):
    request_jsons = json.loads(request.body)
    if request_jsons['type'] == 'sub':
        file_name = './file/result.txt'
    elif request_jsons['type'] == 'complex':
        file_name = './file/result2.txt'
    lines = open(file_name, 'r', encoding='UTF-8').readlines()
    index_line = 0
    data_node = []
    data_edge = []
    test_id = 1
    while index_line < len(lines):
        if lines[index_line].strip() == "State:":
            index_line += 1
            node_num0 = lines[index_line].strip().split('=')[1]
            node_num = int(node_num0[1:])
            node_label = lines[index_line].strip().split('=')[1]
            if node_label == 'S0':
                node_label = 'START'
            index_line += 1
            node_name = lines[index_line].strip().split('=', 1)[1]
            # data.append({"data": {"id": node_name, "label": node_name, "category": node_category.get(node_name, 2)}})
            # data.append({"data": {"id": node_name, "label": node_label,"name":node_name}})
            data_node.append({"id": node_num, "text": node_label, 'name': node_name})
        if lines[index_line].strip() == "Transition:":
            index_line += 1
            name = lines[index_line].strip().split('=', 1)[1]
            index_line += 1
            src0 = lines[index_line].strip().split('=', 1)[1]
            src = int(src0[1:])
            index_line += 1
            tgt0 = lines[index_line].strip().split('=', 1)[1]
            tgt = int(tgt0[1:])
            index_line += 1
            event = lines[index_line].strip().split('=', 1)
            event = event[1] if len(event) > 1 else ""
            index_line += 1
            cond = lines[index_line].strip().split('=', 1)
            cond = cond[1] if len(cond) > 1 else ""
            index_line += 1
            action = lines[index_line].strip().split('=', 1)
            action = action[1] if len(action) > 1 else ""
            edge = {"id": test_id, "from": src, "to": tgt, "text": name, "event": event, "cond": cond,
                    "action": action, "color": "black"}
            # print(edge)
            test_id += 1
            data_edge.append(edge)

        index_line += 1
    # print(data_edge)
    return JsonResponse({**error_code.CLACK_SUCCESS, "data_node": data_node, "data_edge": data_edge})
