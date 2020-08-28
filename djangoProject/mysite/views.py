# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
import os
import json

from django.shortcuts import render


# Create your views here.
def test(request):
    # return JsonResponse({"status": 0, "message": "This is test"})
    os.system('python2 D:/graphTraversal-submit2/execution/project_gui.py')
    # os.system('python C:\\Users\\23789\\Desktop\\test2.py')
    return JsonResponse({"status": 0, "message": "This is test"})


def happy(request):
    # return JsonResponse({"status": 0, "message": "This is test"})
    os.system('python3 E:/Code/301temp/Model3/Model1.py')
    # os.system('python C:\\Users\\23789\\Desktop\\test2.py')
    return JsonResponse({"status": 0, "message": "This is happy"})


def judgeModel(request):
    with open('E:/Code/301temp/djangoProject/out.txt', 'r') as f:
        lines = f.readline().split("\n")
    res = lines[0]

    os.system('python3 E:/Code/Complete/Model3_2/Model3/judgeModelComplete.py')
    # return JsonResponse({"status": 0, "message": "This is judgeModel"})
    return JsonResponse({"result": res})


def addModel(request):
    request_json = json.loads(request.body)
    txtLen = len(request_json)
    with open('E:/Code/Complete/Model3_2/Model3/addTrace.txt', 'w') as f:  # 设置文件对象
        for i in range(txtLen):
            f.write('Trace:\n')
            f.write(request_json[i]['value'].replace('  ', '\n'))# 将字符串写入文件中
            f.write('\n')

    os.system('python3 E:/Code/Complete/Model3_2/Model3/completeModel1.py')
    return JsonResponse({"result": "success"})


def verify(request):
    request_json = json.loads(request.body)
    res = request_json['msg']
    with open('E:/data123.txt', 'w') as f:  # 设置文件对象
        f.write('Transition:\n')
        f.write(res.replace('  ', '\n'))# 将字符串写入文件中
    return JsonResponse({"result": "success"})



