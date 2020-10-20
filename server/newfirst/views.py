import json
import time
import os
import subprocess
import random

from django.http import HttpResponse, JsonResponse
from newfirst.models import Item, Personnel, DesignCriteria, AnalysisRules
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
