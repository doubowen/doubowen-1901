# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import base64
import datetime
import time

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from blueking.component.shortcuts import  get_client_by_user,get_client_by_request
from common.mymako import render_json
from home_application.models import OptLog
from home_application.models import TaskType


@task()
def async_task(bk_biz_id,bk_host_innerip ,bk_cloud_id,task_name,script_param,user_name):
    """
    定义一个 celery 异步任务
    """
    f = open('script/' + task_name + '.sh')
    # f = open('script/test.sh')
    s = f.read()
    # script_content = TaskType.objects.values("script_content").get(task_name=task_name).get('script_content')

    content = base64.b64encode(s)
    start = time.time()

    # 创建操作记录

    client = get_client_by_user(user_name)
    client.set_bk_api_ver('v2')

    res = client.job.fast_execute_script({
        'bk_biz_id': bk_biz_id,
        'ip_list': [{
            "bk_cloud_id": bk_cloud_id,
            "ip": bk_host_innerip
        }],
        'account': 'root',
        'script_type': 1,
        'script_content': content,
        'script_param': script_param,
    })

    if not res.get('result'):
        return render_json(res)

    task_id = res.get('data').get('job_instance_id')
    while not client.job.get_job_instance_status({
        'bk_biz_id': bk_biz_id,
        'job_instance_id': task_id,
    }).get('data').get('is_finished'):
        print 'waiting job finished...'
        time.sleep(1.2)

    res = client.job.get_job_instance_log({
        'bk_biz_id': bk_biz_id,
        'job_instance_id': task_id
    })

    log_content = res['data'][0]['step_results'][0]['ip_logs'][0]['log_content']
    check_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    OptLog.objects.create(
        operator='admin',
        bk_biz_id=bk_biz_id,
        inner_ip=bk_host_innerip,
        opt_at=check_time,
        opt_type=log_content,
    )
    return render_json({
        'result': True,
        'data': {
            'time': datetime.datetime.now().strftime('%Y/%m/%d/%H:%M:%S'),
            'log': log_content
        },
        'message': '%s: elapsed %ss' % (res.get('message'), round(time.time() - start, 2))
    })


def execute_task(bk_biz_id,bk_host_innerip ,bk_cloud_id,task_name,script_param,user_name):
    """
    执行 celery 异步任务

    调用celery任务方法:
        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
        delay(): 简便方法，类似调用普通函数
        apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    async_task.delay(bk_biz_id,bk_host_innerip ,bk_cloud_id,task_name,script_param,user_name)


@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    pass


