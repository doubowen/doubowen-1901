# -*- coding: utf-8 -*-
from django.db import models


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
    job_id = models.CharField(u'作业id', max_length=16)
    opt_at = models.DateTimeField(null=False)
    host_list = models.CharField(u'主机列表', max_length=100)
    job_status = models.CharField(u'作业状态', max_length=100)
    opt_type = models.CharField(u'作业日志', max_length=1000)

    def __unicode__(self):
        return '{}.{}.{}'.format(self.host_list,
                                 self.opt_type,
                                 self.opt_at)

    class Meta:
        verbose_name = '操作记录信息'
        verbose_name_plural = '操作记录信息'