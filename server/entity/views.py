import json
import time
import os
import subprocess

from django.http import HttpResponse, JsonResponse

from entity.models import Trace
from server import error_code
from django.shortcuts import render


# Create your views here.


# 建模
def modeling(request):
    os.system('python3 E:/Code/project301/lwn_Graphic/ConstructModel.py')
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 图形化展示模型
def show_model(request):
    os.system('python3 E:/Code/project301/lwn_Graphic/2020-08.py')
    pp = subprocess.Popen('python3 E:/Code/project301/lwn_Graphic/draw_graph.py')
    time.sleep(10)
    pp.kill()
    return JsonResponse({"status": 0, "message": "ok"})


# 完整性验证
def judge_model(request):
    os.system('python3 E:/Code/project301/lzy_Complete/Model3/judgeModelComplete.py')
    with open('E:/Code/project301/file/out.txt', 'r') as f:
        lines = f.readline().split("\n")
    res = lines[0]
    with open('E:/Code/project301/file/out.txt', 'r') as f:
        test = f.read()
    test = test[62:]
    return JsonResponse({"result": res, "msg": test})


# 模型补全
def add_model(request):
    request_json = json.loads(request.body)
    if (request_json == None):
        return JsonResponse({"status": -1, "message": "内容为空"})
    with open('E:/Code/project301/file/addTrace.txt', 'w') as f:  # 设置文件对象
        for i in range(len(request_json)):
            f.write('Trace:\n')
            f.write(request_json[i]['value'].replace('  ', '\n'))  # 将字符串写入文件中
            f.write('\n')
    os.system('python3 E:/Code/project301/lzy_Complete/Model3/completeModel.py')
    os.system('python3 E:/Code/project301/lwn_Graphic/2020-08.py')

    return JsonResponse({"status": 0, "message": "ok"})


# 安全性验证
def safe_verify(request):
    request_json = json.loads(request.body)
    res = request_json['msg']
    with open('E:/Code/project301/file/target.txt', 'w') as f:  # 设置文件对象
        f.write('Transition:\n')
        f.write(res.replace('  ', '\n'))  # 将字符串写入文件中
    os.system('python2 E:/Code/project301/lxd_Safety/graphTraversal-submit2/execution/project_gui.py')
    return JsonResponse({"status": 0, "message": "ok"})


# 增加场景
def add_trace(request):
    pass


# 修改场景
def edit_trace(request):
    pass


# 删除场景
def delete_trace(request):
    pass


# 查询全部场景
def trace_list(request):
    traces = Trace.objects.all()
    result = [trace.to_dict() for trace in traces]
    return JsonResponse({**error_code.CLACK_SUCCESS, "trace_list": result})

