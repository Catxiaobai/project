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
    item_name = models.TextField(default='', unique=True)
    item_content = models.TextField(default='')
    item_introduction = models.TextField(default='')

    # item_date = models.DateTimeField(default='')
    # item_leader = models.ForeignKey(Personnel, on_delete=models.CASCADE)

    def to_dict(self):
        return {
            'item_id': self.id,
            'item_name': self.item_name,
            'item_content': self.item_content,
            'item_introduction': self.item_introduction,
            # 'item_date': self.item_date,
            # 'item_leader': self.item_leader,
        }


# 设计准则
class DesignCriteria(models.Model):
    name = models.TextField(default='', unique=True)
    describe = models.TextField(default='')
    remark = models.TextField(default='')
    type = models.TextField(default='')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'describe': self.describe,
            'remark': self.remark,
            'type': self.type,
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
    element = models.TextField(default='')
    content = models.TextField(default='')
    type = models.TextField(default='')
    name = models.TextField(default='', unique=True)
    describe = models.TextField(default='')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'element': self.element,
            'type': self.type,
            'describe': self.describe,
            'content': self.content,
        }


# 规则集
class Rules(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
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
            'item': self.item.id
        }


# 实例
class Case(models.Model):
    rule = models.ForeignKey(Rules, on_delete=models.CASCADE)
    case_element = models.TextField(default='')
    case_name = models.TextField(default='', unique=True)
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


# 实例
class Fmea(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, unique=True)
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
            'reason': self.reason,
            'local_influence': self.local_influence,
            'upper_influence': self.upper_influence,
            'system_influence': self.system_influence,
            'influence_level': self.influence_level
        }


# 软件失效分析需求
class Demand(models.Model):
    fmea = models.ForeignKey(Fmea, on_delete=models.CASCADE)
    demand = models.TextField(default='', blank=True)

    def to_dict(self):
        return {
            'id': self.id,
            'demand': self.demand,
            'fmea': self.fmea.id,
        }
