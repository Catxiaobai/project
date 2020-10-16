import json
import time
import os
import subprocess
import random

from django.http import HttpResponse, JsonResponse

from entity.models import Trace, Invalid
from server import error_code
from django.shortcuts import render


# Create your views here.


# 建模
def modeling(request):
    # os.system('python E:/Code/project301/lwn_Graphic/ConstructModel.py')
    # os.system('python E:/Code/project301/lwn_Graphic/2020-08.py')
    filepath = 'E:/Code/project301/file/'
    with open(filepath + 'resultSaveCreate.txt', 'wt+', encoding='utf-8') as f:
        f.write(open(filepath + 'result.txt', 'r', encoding='utf-8').read())
    with open(filepath + 'resultModelSaveCreate.txt', 'wt+', encoding='utf-8') as f:
        f.write(open(filepath + 'resultModel.txt', 'r', encoding='utf-8').read())
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 图形化展示模型（废弃）
def show_model(request):
    os.system('python E:/Code/project301/lwn_Graphic/2020-08.py')
    pp = subprocess.Popen('python E:/Code/project301/lwn_Graphic/draw_graph.py')
    time.sleep(10)
    pp.kill()
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 完整性验证
def judge_model(request):
    os.system('python E:/Code/project301/lzy_Complete/Model3/judgeModelComplete.py')
    with open('E:/Code/project301/file/out.txt', 'r') as f:
        lines = f.readline().split("\n")
    res = lines[0]
    with open('E:/Code/project301/file/out.txt', 'r') as f:
        test = f.read()
    test = test[62:]
    return JsonResponse({**error_code.CLACK_SUCCESS, "result": res, "msg": test})


# 模型补全
def add_model(request):
    request_json = json.loads(request.body)
    if (None == request_json):
        return JsonResponse({**error_code.CLACK_NULL_ERROR})
    with open('E:/Code/project301/file/addTrace.txt', 'w') as f:  # 设置文件对象
        for i in range(len(request_json)):
            f.write('Trace:\n')
            f.write(request_json[i]['value'].replace('  ', '\n'))  # 将字符串写入文件中
            f.write('\n')
    # os.system('python E:/Code/project301/lzy_Complete/Model3/completeModel.py')
    # os.system('python E:/Code/project301/lwn_Graphic/2020-08.py')

    return JsonResponse({**error_code.CLACK_SUCCESS})


# 安全性验证
def safe_verify(request):
    request_json = json.loads(request.body)
    res = request_json['msg']
    with open('E:/Code/project301/file/target.txt', 'w') as f:  # 设置文件对象
        f.write('Transition:\n')
        f.write(res.replace('  ', '\n'))  # 将字符串写入文件中
    os.system('python E:/Code/project301/lxd_Safety/graphTraversal-submit2/execution/project_gui.py')
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 增加场景
def add_trace(request):
    request_json = json.loads(request.body)
    try:
        trace = Trace(trace_name=request_json['name'],
                      trace_content=request_json['content'],
                      trace_describe=request_json['describe'],
                      trace_details=request_json['details'])
        trace.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 修改场景
def edit_trace(request):
    request_json = json.loads(request.body)
    aim_id = request_json['id']
    new_name = request_json['name']
    new_content = request_json['content']
    new_describe = request_json['describe']
    new_details = request_json['details']

    if not Trace.objects.filter(id=aim_id).exists():
        return JsonResponse({**error_code.CLACK_NOT_EXISTS})
    try:
        Trace.objects.filter(id=aim_id).update(trace_name=new_name)
        Trace.objects.filter(id=aim_id).update(trace_content=new_content)
        Trace.objects.filter(id=aim_id).update(trace_describe=new_describe)
        Trace.objects.filter(id=aim_id).update(trace_details=new_details)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": str(e)})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 删除场景
def delete_trace(request):
    request_json = json.loads(request.body)
    aim_id = request_json['trace_id']
    try:
        Trace.objects.get(id=aim_id).delete()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 查询全部场景
def trace_list(request):
    traces = Trace.objects.all()
    result = [trace.to_dict() for trace in traces]
    return JsonResponse({**error_code.CLACK_SUCCESS, "trace_list": result})


# 从txt文件中导入场景
def import_trace(request):
    request_json = json.loads(request.body)
    filename = request_json['name']
    try:
        with open('E:/Code/project301/file/' + filename, 'r', encoding='utf-8') as f:
            original_file = f.read()
            lines = original_file.splitlines()
        index = 0
        if Trace.objects.filter().exists():
            latest_trace = Trace.objects.latest('id')
            latest_id = latest_trace.id
        else:
            latest_id = 1
        while index < len(lines):
            if '0' <= lines[index][0] <= '9':
                index += 1
                new_name = "场景" + str(latest_id)
                latest_id += 1
                new_content = ""
                new_details = ""
                new_describe = ""
                # 判断是否为场景详情
                if lines[index] == "details:":
                    index += 1
                    new_details += lines[index] + '\n'
                    index += 1

                # if '\u4e00' <= lines[index][0] <= '\u9fff':
                #     new_details += lines[index] + '\n'
                #     index += 1
                # 判断是否为场景介绍
                if lines[index] == "title:":
                    index += 1
                    new_describe += lines[index] + '\n'
                    index += 1

                    # 判断是否是trace
                if lines[index] == "Trace:":
                    index += 1
                while index < len(lines) and (lines[index][0] <= '0' or lines[index][0] >= '9'):
                    new_content = new_content + lines[index] + '\n'
                    index += 1
                trace = Trace(trace_name=new_name,
                              trace_content=new_content,
                              trace_details=new_details,
                              trace_describe=new_describe)
                trace.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "content": original_file})


# 增加失效场景
def add_invalid(request):
    request_json = json.loads(request.body)
    try:
        invalid = Invalid(invalid_name=request_json['name'],
                          invalid_content=request_json['content'],
                          invalid_describe=request_json['describe'],
                          invalid_details=request_json['details'])
        invalid.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 修改失效场景
def edit_invalid(request):
    request_json = json.loads(request.body)
    aim_id = request_json['id']
    new_name = request_json['name']
    new_content = request_json['content']
    new_describe = request_json['describe']
    new_details = request_json['details']

    if not Invalid.objects.filter(id=aim_id).exists():
        return JsonResponse({**error_code.CLACK_NOT_EXISTS})
    try:
        Invalid.objects.filter(id=aim_id).update(invalid_name=new_name)
        Invalid.objects.filter(id=aim_id).update(invalid_content=new_content)
        Invalid.objects.filter(id=aim_id).update(invalid_describe=new_describe)
        Invalid.objects.filter(id=aim_id).update(invalid_details=new_details)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": str(e)})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 删除场景
def delete_invalid(request):
    request_json = json.loads(request.body)
    aim_id = request_json['invalid_id']
    try:
        Invalid.objects.get(id=aim_id).delete()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 查询全部场景
def invalid_list(request):
    invalids = Invalid.objects.all()
    result = [invalid.to_dict() for invalid in invalids]
    return JsonResponse({**error_code.CLACK_SUCCESS, "invalid_list": result})


# 从txt文件中导入场景
def import_invalid(request):
    request_json = json.loads(request.body)
    filename = request_json['name']
    try:
        with open('E:/Code/project301/file/' + filename, 'r', encoding='utf-8') as f:
            original_file = f.read()
            lines = original_file.splitlines()
        if Invalid.objects.filter().exists():
            latest_invalid = Invalid.objects.latest('id')
            latest_id = latest_invalid.id
        else:
            latest_id = 1
        index = 0
        while index < len(lines):
            # 判断是否是Transition
            if lines[index] == "Transition:":
                index += 1
                new_name = "风险场景" + str(latest_id)
                latest_id += 1
                new_content = ""
                new_details = "暂无文字表述"
                # 截取第一句放入介绍中
                new_describe = lines[index]
                while index < len(lines) and lines[index] != "Transition:":
                    new_content = new_content + lines[index] + '\n'
                    index += 1
                invalid = Invalid(invalid_name=new_name,
                                  invalid_content=new_content,
                                  invalid_details=new_details,
                                  invalid_describe=new_describe)
                invalid.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "content": original_file})


# 验证失效序列
def verify_invalid(request):
    request_json = json.loads(request.body)
    aim_id = request_json['invalid']['invalid_id']
    aim_invalid = request_json['invalid']['invalid_content']
    print(aim_invalid)
    with open('E:/Code/project301/file/targetInvalid.txt', 'w') as f:  # 设置文件对象
        f.write('Transition:\n')
        f.write(aim_invalid)
    try:
        os.system('py -2 E:/Code/project301/lxd_Safety/graphTraversal-submit2/execution/project_gui.py')
        # os.system('py -2 E:/Code/project301/lxd_Safety/newVerify/Main.py')

        with open('E:/Code/project301/file/path.txt') as f:
            lines = f.read()
        if len(lines) > 2:
            # print("len长度"+len(lines))
            a = 0
        else:
            a = 1
        # a = random.randint(0, 1)
        if a == 0:
            Invalid.objects.filter(id=aim_id).update(invalid_verify="danger")
            res = 'danger'
        elif a == 1:
            Invalid.objects.filter(id=aim_id).update(invalid_verify="safe")
            res = 'safe'
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, 'res': res})


# 重置失效序列验证
def reset_verify(request):
    request_json = json.loads(request.body)
    try:
        for i in range(0, len(request_json)):
            aim_id = request_json[i]['invalid_id']
            if not Invalid.objects.filter(id=aim_id).exists():
                return JsonResponse({**error_code.CLACK_NOT_EXISTS})
            Invalid.objects.filter(id=aim_id).update(invalid_verify="null")
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 传递模型数据
def deliver_model(request):
    file_name = 'E:/Code/project301/file/result.txt'
    # file_name = 'E:/Code/project301/file/resultModel.txt'
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


# 验证对模型的添加操作是否合理
def verify_add(request):
    request_json = json.loads(request.body)
    # # 添加的信息
    # add = request_json['add']
    # # 剩下的信息
    # total = request_json['total']
    # print('add:'+delete)
    # print('total:'+total)
    try:
        a = random.randint(0, 2)
        if a == 0:
            res = 'error'
        elif a == 2:
            res = 'success'
        elif a == 1:
            res = 'warning'
    # 验证程序
    #         res = ''
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "result": res})


# 验证对模型的删除操作是否合理
def verify_del(request):
    request_json = json.loads(request.body)
    # 删除的信息
    delete = []
    delete.append(json.loads(request_json['delete']))
    # 剩下的信息
    node = json.loads(request_json['total'])['nodeDataArray']
    edge = json.loads(request_json['total'])['linkDataArray']
    # print('delete:')
    # print(delete)
    # print(node)
    # print('edge:')
    # print(edge)
    filepath = 'E:/Code/project301/file/'
    try:
        data_list1 = node
        result = ''
        for data_dict in data_list1:
            if 'text' in data_dict.keys():
                if data_dict['text'] == "S0":
                    data_dict['text'] = "START"
                result = result + 'State:' + '\n' + '\t' + 'name=' + data_dict[
                    'text'] + '\n'

        data_list2 = edge
        # print(data_list2)
        for data_dict in data_list2:
            if str(data_dict['from']) == '0':
                data_dict['from'] = 'TART'
            elif str(data_dict['to']) == '0':
                data_dict['to'] = 'TART'
            result = result + 'Transition:' + '\n' \
                     + '\t' + 'name=' + str(data_dict['text']) + '\n' \
                     + '\t' + 'src=' + 'S' + str(data_dict['from']) + '\n' \
                     + '\t' + 'tgt=' + 'S' + str(data_dict['to']) + '\n' \
                     + '\t' + 'event=' + str(data_dict['event']) + '\n' \
                     + '\t' + 'condition=' + str(data_dict['cond']) + '\n' \
                     + '\t' + 'action=' + str(data_dict['action']) + '\n'
            # print(result)
        with open(filepath + 'resultModel.txt', 'wt+', encoding='utf-8') as f:
            f.write(result)

        data_list3 = node
        result = ''
        for data_dict in data_list3:
            if 'text' in data_dict.keys():
                if data_dict['text'] == "START":
                    data_dict['text'] = "S0"
                result = result + 'State:' + '\n' + '\t' + 'label=' + data_dict[
                    'text'] + '\n' + '\t' + 'name=' + data_dict['name'] + '\n'

        data_list4 = edge
        # print(data_list2)
        for data_dict in data_list4:
            if str(data_dict['from']) == 'TART':
                data_dict['from'] = '0'
            elif str(data_dict['to']) == 'TART':
                data_dict['to'] = '0'
            result = result + 'Transition:' + '\n' \
                     + '\t' + 'name=' + str(data_dict['text']) + '\n' \
                     + '\t' + 'src=' + 'S' + str(data_dict['from']) + '\n' \
                     + '\t' + 'tgt=' + 'S' + str(data_dict['to']) + '\n' \
                     + '\t' + 'event=' + str(data_dict['event']) + '\n' \
                     + '\t' + 'condition=' + str(data_dict['cond']) + '\n' \
                     + '\t' + 'action=' + str(data_dict['action']) + '\n'
            # print(result)
        with open(filepath + 'result.txt', 'wt+', encoding='utf-8') as f:
            f.write(result)

        # 验证程序
        os.system('python E:/Code/project301/lzy_Complete/Model3/judge/judgeFeasibility/delete.py')

        with open(filepath + 'judgeResult.txt') as f:
            a = int(f.read())
        if a == 0:
            res = 'error'
        elif a == 1:
            res = 'warning'
        elif a == 2:
            res = 'success'

    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "result": res})


# 验证模型的完整性
def verify_complete(request):
    file_name = 'E:/Code/project301/file/result.txt'
    lines = open(file_name, 'r', encoding='UTF-8').readlines()
    index_line = 0
    data_node = []
    data_edge = []
    data_node_add = []
    data_edge_add = []
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
            test_id += 1
            data_edge.append(edge)

        index_line += 1
    # print(1)
    # E:\Code\project301\lzy_Complete\Model5\judgeFeasibility
    os.system('python E:/Code/project301/lzy_Complete/Model5/judgeFeasibility/judgeModelComplete.py')
    file_name2 = 'E:/Code/project301/file/outNew.txt'
    lines = open(file_name2, 'r', encoding='UTF-8').readlines()
    index_line = 0
    res = 0
    print(lines[0])
    if lines[0] == 'Y\n':
        res = 'Y'
    elif lines[0] == 'N\n':
        res = 'N'
        index_line += 1
        while index_line < len(lines):
            edge_name = lines[index_line].strip().split(',')[0]
            edge_num = int(edge_name[1:])
            src = lines[index_line].strip().split(',')[1]
            src0 = int(src[2:])
            src = src.replace(' ', '')
            tgt = lines[index_line].strip().split(',')[2]
            tgt0 = int(tgt[2:])
            tgt = tgt.replace(' ', '')
            event = lines[index_line].strip().split(',')[3].split('=', 1)[1]
            cond = lines[index_line].strip().split(',')[4].split('=', 1)[1]
            action = lines[index_line].strip().split(',')[5].split('=', 1)[1]
            t = 1  # 判断增加节点是否需要新添
            for data_dict in data_node:
                if src0 == data_dict['id']:
                    t = 0
            if t == 1:
                data_node_add.append({"id": src0, "text": src, 'name': src, 'color': 'pink'})
                data_node.append({"id": src0, "text": src, 'name': src, 'color': 'pink'})
            t = 1
            for data_dict in data_node:
                if tgt0 == data_dict['id']:
                    t = 0
            if t == 1:
                data_node_add.append({"id": tgt0, "text": tgt, 'name': tgt})
                data_node.append({"id": tgt0, "text": tgt, 'name': tgt, 'color': 'pink'})
            edge = {"id": edge_num, "from": src0, "to": tgt0, "text": edge_name, "event": event, "cond": cond,
                    "action": action, "color": 'pink'}
            index_line += 1
            data_edge_add.append(edge)
            data_edge.append(edge)
    # print(data_edge)
    # print(data_node)
    return JsonResponse({**error_code.CLACK_SUCCESS, "data_node": data_node, "data_edge": data_edge,
                         "data_node_add": data_node_add, "data_edge_add": data_edge_add, "res": res})


# 返回前端失效场景的复现路径
def verify_safe_result(request):
    file_name = 'E:/Code/project301/file/path.txt'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            lines = f.read()
        list_path = list(map(lambda a: int(a), lines[1:-1].split(',')))
        print(list_path)
        data_path = list_path
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "data_path": data_path})


# 一次性验证多个失效序列
def verify_select_invalid(request):
    request_json = json.loads(request.body)
    try:
        for i in range(0, len(request_json)):
            aim_id = request_json[i]['invalid_id']
            aim_invalid = request_json[i]['invalid_content']
            # print(aim_invalid)
            if not Invalid.objects.filter(id=aim_id).exists():
                return JsonResponse({**error_code.CLACK_NOT_EXISTS})
            with open('E:/Code/project301/file/targetInvalid.txt', 'w') as f:  # 设置文件对象
                f.write('Transition:\n')
                f.write(aim_invalid)
            os.system('py -2 E:/Code/project301/lxd_Safety/graphTraversal-submit2/execution/project_gui.py')
            with open('E:/Code/project301/file/path.txt') as f:
                lines = f.read()
            if len(lines) > 2:
                # print("len长度"+len(lines))
                # a = 0
                Invalid.objects.filter(id=aim_id).update(invalid_verify="danger")
            else:
                # a = 1
                Invalid.objects.filter(id=aim_id).update(invalid_verify="success")
            # a = random.randint(0, 1)
            # if a == 0:
            #
            # elif a == 1:
            #
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 模型还原成单次编辑前的样子
def recovery_model(request):
    filepath = 'E:/Code/project301/file/'
    with open(filepath + 'result.txt', 'wt+', encoding='utf-8') as f:
        f.write(open(filepath + 'resultSave.txt', 'r', encoding='utf-8').read())
    with open(filepath + 'resultModel.txt', 'wt+', encoding='utf-8') as f:
        f.write(open(filepath + 'resultModelSave.txt', 'r', encoding='utf-8').read())
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 保存编辑前的模型样子
def save_model(request):
    filepath = 'E:/Code/project301/file/'
    with open(filepath + 'resultSave.txt', 'wt+', encoding='utf-8') as f:
        f.write(open(filepath + 'result.txt', 'r', encoding='utf-8').read())
    with open(filepath + 'resultModelSave.txt', 'wt+', encoding='utf-8') as f:
        f.write(open(filepath + 'resultModel.txt', 'r', encoding='utf-8').read())
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 补全完整性验证的结果
def save_integrity_verification(request):
    request_json = json.loads(request.body)
    # print(request_json['total']['nodeDataArray'])
    # test = json.loads(request_json['total'])
    # print(test)
    node = request_json['total']['nodeDataArray']
    edge = request_json['total']['linkDataArray']
    # print('delete:')
    # print(delete)
    # print(node)
    # print('edge:')
    # print(edge)
    filepath = 'E:/Code/project301/file/'
    try:
        data_list1 = node
        result = ''
        for data_dict in data_list1:
            if 'text' in data_dict.keys():
                if data_dict['text'] == "S0":
                    data_dict['text'] = "START"
                result = result + 'State:' + '\n' + '\t' + 'name=' + data_dict[
                    'text'] + '\n'

        data_list2 = edge
        # print(data_list2)
        for data_dict in data_list2:
            if str(data_dict['from']) == '0':
                data_dict['from'] = 'TART'
            elif str(data_dict['to']) == '0':
                data_dict['to'] = 'TART'
            result = result + 'Transition:' + '\n' \
                     + '\t' + 'name=' + str(data_dict['text']) + '\n' \
                     + '\t' + 'src=' + 'S' + str(data_dict['from']) + '\n' \
                     + '\t' + 'tgt=' + 'S' + str(data_dict['to']) + '\n' \
                     + '\t' + 'event=' + str(data_dict['event']) + '\n' \
                     + '\t' + 'condition=' + str(data_dict['cond']) + '\n' \
                     + '\t' + 'action=' + str(data_dict['action']) + '\n'
            # print(result)
        with open(filepath + 'resultModel.txt', 'wt+', encoding='utf-8') as f:
            f.write(result)

        data_list3 = node
        result = ''
        for data_dict in data_list3:
            if 'text' in data_dict.keys():
                if data_dict['text'] == "START":
                    data_dict['text'] = "S0"
                result = result + 'State:' + '\n' + '\t' + 'label=' + data_dict[
                    'text'] + '\n' + '\t' + 'name=' + data_dict['name'] + '\n'

        data_list4 = edge
        # print(data_list2)
        for data_dict in data_list4:
            if str(data_dict['from']) == 'TART':
                data_dict['from'] = '0'
            elif str(data_dict['to']) == 'TART':
                data_dict['to'] = '0'
            result = result + 'Transition:' + '\n' \
                     + '\t' + 'name=' + str(data_dict['text']) + '\n' \
                     + '\t' + 'src=' + 'S' + str(data_dict['from']) + '\n' \
                     + '\t' + 'tgt=' + 'S' + str(data_dict['to']) + '\n' \
                     + '\t' + 'event=' + str(data_dict['event']) + '\n' \
                     + '\t' + 'condition=' + str(data_dict['cond']) + '\n' \
                     + '\t' + 'action=' + str(data_dict['action']) + '\n'
            # print(result)
        with open(filepath + 'result.txt', 'wt+', encoding='utf-8') as f:
            f.write(result)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 补全完整性的点或边
def save_node_and_link(request):
    request_json = json.loads(request.body)
    file_name = 'E:/Code/project301/file/result.txt'
    lines = open(file_name, 'r', encoding='UTF-8').readlines()
    index_line = 0
    Sr = ''
    Sm = ''
    Tr = ''
    Tm = ''
    while index_line < len(lines):
        if lines[index_line].strip() == "State:":
            index_line += 1
            node_num0 = lines[index_line].strip().split('=')[1]
            node_num = int(node_num0[1:])

            node_label = lines[index_line].strip().split('=')[1]
            index_line += 1
            node_name = lines[index_line].strip().split('=', 1)[1]
            # data.append({"data": {"id": node_name, "label": node_name, "category": node_category.get(node_name, 2)}})
            # data.append({"data": {"id": node_name, "label": node_label,"name":node_name}})
            Sr = Sr + 'State:' + '\n' + '\t' + 'label=' + node_num0 + '\n' + '\t' + 'name=' + node_name + '\n'
            if node_num0 == "S0":
                node_num0 = "START"
            Sm = Sm + 'State:' + '\n' + '\t' + 'name=' + node_num0 + '\n'
        if lines[index_line].strip() == "Transition:":
            index_line += 1
            name = lines[index_line].strip().split('=', 1)[1]
            name0 = int(name[1:])
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
            Tr = Tr + 'Transition:' + '\n' \
                 + '\t' + 'name=' + name + '\n' \
                 + '\t' + 'src=' + src0 + '\n' \
                 + '\t' + 'tgt=' + tgt0 + '\n' \
                 + '\t' + 'event=' + event + '\n' \
                 + '\t' + 'condition=' + cond + '\n' \
                 + '\t' + 'action=' + action + '\n'
            if src0 == "S0":
                src0 = "START"
            if tgt0 == "S0":
                tgt0 = "START"
            Tm = Tm + 'Transition:' + '\n' \
                 + '\t' + 'name=' + name + '\n' \
                 + '\t' + 'src=' + src0 + '\n' \
                 + '\t' + 'tgt=' + tgt0 + '\n' \
                 + '\t' + 'event=' + event + '\n' \
                 + '\t' + 'condition=' + cond + '\n' \
                 + '\t' + 'action=' + action + '\n'
        index_line += 1
    if 'node' in request_json:
        node = request_json['node']
        print(node)
        if 'text' in node.keys():

            Sr = Sr + 'State:' + '\n' + '\t' + 'label=' + node[
                'text'] + '\n' + '\t' + 'name=' + node['name'] + '\n'
            if node['text'] == "S0":
                node['text'] = "START"
            Sm = Sm + 'State:' + '\n' + '\t' + 'name=' + node[
                'text'] + '\n'
            print(Sr)
            print(Sm)
        # print(Sr)
        # print(Sm)
    elif 'edge' in request_json:
        edge = request_json['edge']
        print(edge)
        Tr = Tr + 'Transition:' + '\n' \
             + '\t' + 'name=' + str(edge['text']) + '\n' \
             + '\t' + 'src=' + 'S' + str(edge['from']) + '\n' \
             + '\t' + 'tgt=' + 'S' + str(edge['to']) + '\n' \
             + '\t' + 'event=' + str(edge['event']) + '\n' \
             + '\t' + 'condition=' + str(edge['cond']) + '\n' \
             + '\t' + 'action=' + str(edge['action']) + '\n'
        if str(edge['from']) == '0':
            edge['from'] = 'TART'
        elif str(edge['to']) == '0':
            edge['to'] = 'TART'
        Tm = Tm + 'Transition:' + '\n' \
             + '\t' + 'name=' + str(edge['text']) + '\n' \
             + '\t' + 'src=' + 'S' + str(edge['from']) + '\n' \
             + '\t' + 'tgt=' + 'S' + str(edge['to']) + '\n' \
             + '\t' + 'event=' + str(edge['event']) + '\n' \
             + '\t' + 'condition=' + str(edge['cond']) + '\n' \
             + '\t' + 'action=' + str(edge['action']) + '\n'
    with open('E:/Code/project301/file/result.txt', 'wt+', encoding='utf-8') as f:
        f.write(Sr + Tr)
    with open('E:/Code/project301/file/resultModel.txt', 'wt+', encoding='utf-8') as f:
        f.write(Sm + Tm)
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 还原为刚建模的样子
def recovery_origin_model(request):
    filepath = 'E:/Code/project301/file/'
    with open(filepath + 'result.txt', 'wt+', encoding='utf-8') as f:
        f.write(open(filepath + 'resultSaveCreate.txt', 'r', encoding='utf-8').read())
    with open(filepath + 'resultModel.txt', 'wt+', encoding='utf-8') as f:
        f.write(open(filepath + 'resultModelSaveCreate.txt', 'r', encoding='utf-8').read())
    return JsonResponse({**error_code.CLACK_SUCCESS})
