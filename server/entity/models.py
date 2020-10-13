from django.db import models

# Create your models here.


# 使用场景
class Trace(models.Model):
    trace_name = models.TextField(default='', unique=True)
    trace_content = models.TextField(default='')
    trace_details = models.TextField(default='')
    trace_describe = models.TextField(default='')

    def to_dict(self):
        return {
            'trace_id': self.id,
            'trace_name': self.trace_name,
            'trace_content': self.trace_content,
            'trace_details': self.trace_details,
            'trace_describe': self.trace_describe
        }


# 失效场景
class Invalid(models.Model):
    invalid_name = models.TextField(default='', unique=True)
    invalid_content = models.TextField(default='')
    invalid_details = models.TextField(default='')
    invalid_describe = models.TextField(default='')
    invalid_verify = models.TextField(default='null')
    invalid_type = models.TextField(default='')

    def to_dict(self):
        return {
            'invalid_id': self.id,
            'invalid_name': self.invalid_name,
            'invalid_content': self.invalid_content,
            'invalid_details': self.invalid_details,
            'invalid_describe': self.invalid_describe,
            'invalid_verify': self.invalid_verify,
            'invalid_type': self.invalid_type,
        }


# # 失效（安全性）验证
# class InvalidVerify(models.Model):
#     invalid_id = models.ForeignKey(Invalid, on_delete=models.CASCADE, null=False)
#     verify_result = models.BooleanField()


# 项目表
class Item(models.Model):
    item_name = models.TextField(default='', unique=True)
    item_content = models.TextField(default='')
    item_describe = models.TextField(default='')

    def to_dict(self):
        return {
            'invalid_id': self.id,
            'item_name': self.item_name,
            'item_content': self.item_content,
            'item_describe': self.item_describe,
        }


# 项目-使用场景表
class ItemTrace(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    trace = models.ForeignKey(Trace, on_delete=models.CASCADE)
    relation_describe = models.TextField(default='')


# 项目-失效场景表
class ItemInvalid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    invalid = models.ForeignKey(Invalid, on_delete=models.CASCADE)
    relation_describe = models.TextField(default='')