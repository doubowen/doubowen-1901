# -*- coding: utf-8 -*-
from django.db import models


# class Scripts(models.Model):
#     """业务信息"""
#
#     script_name = models.CharField(u'脚本名称', max_length=64)
#     script_desc = models.CharField(u'脚本说明', max_length=64, blank=True)
#     script_content = models.CharField(u'脚本内容', max_length=1024, blank=True)
#     script_param = models.CharField(u'默认参数', max_length=64, blank=True)
#
#     def __unicode__(self):
#         return '{}.{}.{}.{}'.format(self.script_name,
#                                     self.script_desc,
#                                     self.script_content,
#                                     self.script_param)


class TaskType(models.Model):
    """任务信息"""

    task_name = models.CharField(u'任务名称', max_length=64)
    task_desc = models.CharField(u'任务说明', max_length=64, blank=True, null=True)
    script_content = models.TextField(u'脚本内容', null=True)
    script_param = models.CharField(u'脚本参数', max_length=64, blank=True, null=True)

    def __unicode__(self):
        return '{}.{}.{}.{}'.format(self.task_name,
                                    self.task_desc,
                                    self.script_content,
                                    self.script_param)


class OptLog(models.Model):
    """操作记录信息"""
    operator = models.CharField(u'操作用户', max_length=128)
    bk_biz_id = models.CharField(u'业务', max_length=16)
    inner_ip = models.GenericIPAddressField(u'内网IP')
    opt_at = models.CharField(u'操作时间', max_length=100)
    opt_type = models.CharField(u'操作结果', max_length=1000)

    def __unicode__(self):
        return '{}.{}.{}'.format(self.inner_ip,
                                 self.opt_type,
                                 self.opt_at)

    class Meta:
        verbose_name = '操作记录信息'
        verbose_name_plural = '操作记录信息'