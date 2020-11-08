from django.db import models


# Create your models here.


# 人员
class Personnel(models.Model):
    name = models.TextField(default='', unique=True)
    age = models.IntegerField(default=0, blank=True)
    gender = models.TextField(default='', blank=True)
    account = models.TextField(default='', unique=True)
    password = models.TextField(default='')
    authority = models.IntegerField(default='')
    team = models.TextField(default='', blank=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'account': self.account,
            'password': self.password,
            'authority': self.authority,
            'team': self.team
        }


# 项目
class Item(models.Model):
    name = models.TextField(default='', unique=True)
    software = models.TextField(default='')
    team = models.TextField(default='')
    level = models.TextField(default='')
    path = models.TextField(default='')

    # item_date = models.DateTimeField(default='')
    # item_leader = models.ForeignKey(Personnel, on_delete=models.CASCADE)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'software': self.software,
            'team': self.team,
            'level': self.level,
            'path': self.path,
        }


# 设计准则
class DesignCriteria(models.Model):
    name = models.TextField(default='')
    describe = models.TextField(default='')
    # remark = models.TextField(default='', blank=True)
    type = models.TextField(default='')
    element = models.TextField(default='')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'describe': self.describe,
            # 'remark': self.remark,
            'type': self.type,
            'element': self.element
        }


# 分析规则
class AnalysisRules(models.Model):
    remark = models.TextField(default='')
    type = models.TextField(default='')
    name = models.TextField(default='', unique=True)
    describe = models.TextField(default='')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'describe': self.describe,
            'remark': self.remark,
            'type': self.type,
        }


# 场景
class Scenes(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    element = models.TextField(default='')
    content = models.TextField(default='')
    type = models.TextField(default='')
    name = models.TextField(default='')
    describe = models.TextField(default='')

    def to_dict(self):
        type2 = ''
        if self.type == 'sub':
            type2 = '子场景'
        elif self.type == 'complex':
            type2 = '综合场景'
        return {
            'id': self.id,
            'name': self.name,
            'element': self.element,
            'type': self.type,
            'type2': type2,
            'describe': self.describe,
            'content': self.content,
            'item': self.item.id,
            'model_name': self.item.name + '的' + self.element
        }


# 规则集
class Rules(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    remark = models.TextField(default='')
    type = models.TextField(default='')
    name = models.TextField(default='')
    describe = models.TextField(default='')
    belong = models.TextField(default='')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'describe': self.describe,
            'remark': self.remark,
            'type': self.type,
            'item': self.item.id,
            'belong': self.belong,

        }


# 实例
class Case(models.Model):
    rule = models.ForeignKey(Rules, on_delete=models.CASCADE)
    case_element = models.TextField(default='')
    case_name = models.TextField(default='')
    case_content = models.TextField(default='')
    case_describe = models.TextField(default='')
    verify_result = models.TextField(default='未检验')
    last_verify_result = models.TextField(default='未检验')
    verify_count = models.IntegerField(default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.case_name,
            'content': self.case_content,
            'describe': self.case_describe,
            'element': self.case_element,
            'result': self.verify_result,
            'last_result': self.last_verify_result,
            'rule_id': self.rule.id,
            'count': self.verify_count,
            'rule_describe': self.rule.describe
        }


# fmea失效分析
class Fmea(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    case_element = models.TextField(default='', blank=True)
    case_name = models.TextField(default='', blank=True)
    case_content = models.TextField(default='', blank=True)
    case_describe = models.TextField(default='', blank=True)
    improve = models.TextField(default='', blank=True)
    reason = models.TextField(default='', blank=True)
    describe = models.TextField(default='', blank=True)
    local_influence = models.TextField(default='', blank=True)
    upper_influence = models.TextField(default='', blank=True)
    system_influence = models.TextField(default='', blank=True)
    influence_level = models.TextField(default='', blank=True)
    ignore = models.BooleanField(default=False, blank=True)

    def to_dict(self):
        return {
            'id': self.id,
            'improve': self.improve,
            'case_name': self.case_name,
            'case_content': self.case_content,
            'case_element': self.case_element,
            'case_describe': self.case_describe,
            'describe': self.describe,
            'reason': self.reason,
            'local_influence': self.local_influence,
            'upper_influence': self.upper_influence,
            'system_influence': self.system_influence,
            'influence_level': self.influence_level,
            'ignore': self.ignore,
            'item': self.item.id
        }


# 软件失效分析需求
class Demand(models.Model):
    fmea = models.OneToOneField(Fmea, on_delete=models.CASCADE)
    demand = models.TextField(default='', blank=True)

    def to_dict(self):
        return {
            'id': self.id,
            'demand': self.demand,
            'improve': self.fmea.improve,
            'describe': self.fmea.case_describe,
            'fmea': self.fmea.id,
        }


# 项目设计准则集
class Design(models.Model):
    name = models.TextField(default='', blank=True)
    describe = models.TextField(default='')
    type = models.TextField(default='')
    element = models.TextField(default='')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    belong = models.TextField(default='')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'describe': self.describe,
            'type': self.type,
            'element': self.element,
            'item': self.item.id,
            'belong': self.belong
        }


# 设计核查
class DesignCheck(models.Model):
    design = models.OneToOneField(Design, on_delete=models.CASCADE)
    apply = models.TextField(default='', blank=True)
    suitable = models.TextField(default='', blank=True)
    problem = models.TextField(default='', blank=True)

    def to_dict(self):
        return {
            'id': self.id,
            'problem': self.problem,
            'apply': self.apply,
            'suitable': self.suitable,
            'design': self.design.id,
            'describe': self.design.describe,
            'type': self.design.type,
            'element': self.design.element,
            'item': self.design.item_id
        }


# 设计完善
class DesignComplete(models.Model):
    designCheck = models.OneToOneField(DesignCheck, on_delete=models.CASCADE)
    complete = models.TextField(default='', blank=True)

    def to_dict(self):
        return {
            'id': self.id,
            'complete': self.complete,
            'check': self.designCheck.id,
            'describe': self.designCheck.design.describe,
            'type': self.designCheck.design.type,
            'element': self.designCheck.design.element,
            'problem': self.designCheck.problem,
            'item': self.designCheck.design.item_id
        }


# 模型列表
class Models(models.Model):
    scenes = models.ForeignKey(Scenes, on_delete=models.CASCADE)
    name = models.TextField(default='')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'scenes_element': self.scenes.element,
            'scenes_type': self.scenes.type,
            'scenes_describe': self.scenes.describe,
            'scenes_content': self.scenes.content,
            'scenes_name': self.scenes.name,
            'item_id': self.scenes.item.id,
            'item_name': self.scenes.item.name,
        }


# 模型列表
class FTA(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    number = models.IntegerField(default='')
    path = models.TextField(default='')

    def to_dict(self):
        return {
            'id': self.id,
            'item': self.item.id,
            'number': self.number,
            'path': self.path,
        }