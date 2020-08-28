# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
import os
import json
from django.shortcuts import render


# Create your views here.
# 建模
def modeling(request):
    os.system('python3 E:/Code/project301/lwn_Graphic/ConstructModel.py')
    return JsonResponse({"status": 0, "message": "ok"})


# 图形化展示模型
def showModel(request):
    os.system('python3 E:/Code/project301/lwn_Graphic/draw_graph.py')
    return JsonResponse({"status": 0, "message": "ok"})


# 完整性验证
def judgeModel(request):
    os.system('python3 E:/Code/project301/lzy_Complete/Model3/judgeModelComplete.py')
    with open('E:/Code/project301/file/out.txt', 'r') as f:
        lines = f.readline().split("\n")
    res = lines[0]
    return JsonResponse({"result": res})


# 模型补全
def addModel(request):
    request_json = json.loads(request.body)
    with open('E:/Code/project301/file/addTrace.txt', 'w') as f:  # 设置文件对象
        for i in range(len(request_json)):
            f.write('Trace:\n')
            f.write(request_json[i]['value'].replace('  ', '\n'))  # 将字符串写入文件中
            f.write('\n')
    os.system('python3 E:/Code/project301/lzy_Complete/Model3/completeModel.py')
    return JsonResponse({"status": 0, "message": "ok"})


# 安全性验证
def safeVerify(request):
    request_json = json.loads(request.body)
    res = request_json['msg']
    with open('E:/Code/project301/file/target.txt', 'w') as f:  # 设置文件对象
        f.write('Transition:\n')
        f.write(res.replace('  ', '\n'))  # 将字符串写入文件中
    os.system('python2 E:/Code/project301/lxd_Safety/graphTraversal-submit2/execution/project_gui.py')
    return JsonResponse({"status": 0, "message": "ok"})











