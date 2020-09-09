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


