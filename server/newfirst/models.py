from django.db import models


# Create your models here.


# 人员
class Personnel(models.Model):
    person_name = models.TextField(default='', unique=True)
    person_age = models.IntegerField(default='')
    person_gender = models.TextField(default='')
    person_account = models.TextField(default='')
    person_password = models.TextField(default='')
    person_authority = models.IntegerField(default='')

    def to_dict(self):
        return {
            'person_id': self.id,
            'person_name': self.person_name,
            'person_age': self.person_age,
            'person_gender': self.person_gender,
            'person_account': self.person_account,
            'person_password': self.person_password,
            'person_authority': self.person_authority,
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
        return {
            'id': self.id,
            'name': self.name,
            'element': self.element,
            'type': self.type,
            'describe': self.describe,
            'content': self.content,
            'item': self.item.id
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
            'belong': self.belong
        }


# 实例
class Case(models.Model):
    rule = models.ForeignKey(Rules, on_delete=models.CASCADE)
    case_element = models.TextField(default='')
    case_name = models.TextField(default='')
    case_content = models.TextField(default='')
    case_describe = models.TextField(default='')
    verify_result = models.TextField(default='unverified')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.case_name,
            'content': self.case_content,
            'describe': self.case_describe,
            'element': self.case_element,
            'verify': self.verify_result,
            'rule_id': self.rule.id
        }


# fmea失效分析
class Fmea(models.Model):
    case = models.OneToOneField(Case, on_delete=models.CASCADE)
    improve = models.TextField(default='', blank=True)
    reason = models.TextField(default='', blank=True)
    local_influence = models.TextField(default='', blank=True)
    upper_influence = models.TextField(default='', blank=True)
    system_influence = models.TextField(default='', blank=True)
    influence_level = models.TextField(default='', blank=True)

    def to_dict(self):
        return {
            'id': self.id,
            'improve': self.improve,
            'case': self.case.id,
            'describe': self.case.case_describe,
            'reason': self.reason,
            'local_influence': self.local_influence,
            'upper_influence': self.upper_influence,
            'system_influence': self.system_influence,
            'influence_level': self.influence_level
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
            'describe': self.fmea.case.case_describe,
            'fmea': self.fmea.id,
        }


# 项目设计准则集
class Design(models.Model):
    name = models.TextField(default='', blank=True)
    describe = models.TextField(default='')
    type = models.TextField(default='')
    element = models.TextField(default='')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'describe': self.describe,
            'type': self.type,
            'element': self.element,
            'item': self.item.id
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