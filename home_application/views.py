# -*- coding: utf-8 -*-

from common.mymako import render_mako_context, render_json, render_mako_tostring
from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from common.log import logger
from home_application import celery_tasks
from home_application.models import TaskType, OptLog
import time

from biz_utils import get_app_by_user
from django.http import HttpResponse, JsonResponse


def home(request):
    """
    首页
    """
    client = get_client_by_request(request)
    print(1)
    client.set_bk_api_ver('v2')
    # 根据权限查询业务列表
    bk_biz_list = get_app_by_user(request.COOKIES['bk_token'])
    for x in bk_biz_list:
        if x.get("app_name") == u'\u8d44\u6e90\u6c60' or x.get("app_name") == 'Resource pool':
            bk_biz_list.remove(x)
            break
    task_list = TaskType.objects.all()
    bk_host_list = get_host(request,bk_biz_list[0]['app_id'])
    return render_mako_context(request, '/home_application/home1.html', {
        'bk_biz_list': bk_biz_list,
        'task_list': task_list,
        'bk_host_list':bk_host_list,
    })
    # client = get_client_by_request(request)
    # client.set_bk_api_ver('v2')
    # # 查询业务
    # res = client.cc.search_business()
    #
    # if res.get('result', False):
    #     bk_biz_list = res.get('data').get('info')
    # else:
    #     logger.error(u"请求业务列表失败：%s" % res.get('message'))
    #     bk_biz_list = []
    # task_list = TaskType.objects.all()
    # bk_host_list = get_host(request, bk_biz_list[0]['bk_biz_id'])
    # return render_mako_context(request, '/home_application/home1.html', {
    #     'bk_biz_list': bk_biz_list,
    #     'task_list': task_list,
    #     'bk_host_list': bk_host_list,
    # })


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def test(request):

    t = time.localtime()
    print t
    print t.tm_year
    print t[0]
    g = (i for i in range(5))
    type(g)
    print type(g)
    x='abcd'
    print(list(map(list, x)))
    return render_json({'result':True,'msg':'测试接口成功','code':'000000'})


def get_hosts(request):
    """
    获取主机
    """
    client = get_client_by_request(request)
    client.set_bk_api_ver('v2')
    bk_biz_id = request.GET["bk_biz_id"]
    res = client.cc.search_host({
        "page": {"start": 0, "limit": 10, "sort": "bk_host_id"},
        "ip": {
            "flag": "bk_host_innerip|bk_host_outerip",
            "exact": 1,
            "data": []
        },
        "condition": [
            {
                "bk_obj_id": "host",
                "fields": [
                ],
                "condition": []
            },
            {
                "bk_obj_id": "biz",
                "fields": [
                    "default",
                    "bk_biz_id",
                    "bk_biz_name",
                ],
                "condition": [
                    {
                        "field": "bk_biz_id",
                        "operator": "$eq",
                        "value": int(bk_biz_id)
                    }
                ]
            }
        ]
    })

    if res.get('result', False):
        bk_host_list = res.get('data').get('info')
    else:
        bk_host_list = []
        logger.error(u"请求主机列表失败：%s" % res.get('message'))

    bk_host_list = [
        {
            'bk_host_innerip': host['host']['bk_host_innerip'],
            'bk_host_name': host['host']['bk_host_name'],
            'bk_host_id': host['host']['bk_host_id'],
            'bk_os_type': host['host']['bk_os_type'],
            'bk_os_name': host['host']['bk_os_name'],
            'bk_cloud_id': host['host']['bk_cloud_id'][0]['bk_inst_id'],
            'bk_cloud_name': host['host']['bk_cloud_id'][0]['bk_inst_name'],
            'bk_set_name': ' '.join(map(lambda x: x['bk_set_name'], host['set'])[:1]),
            'bk_module_name': ' '.join(map(lambda x: x['bk_module_name'], host['module'])[:1]),
        }
        for host in bk_host_list
    ]
    data = render_mako_tostring('/home_application/tbody-ip.html', {
        'bk_host_list': bk_host_list
    })
    return render_json({
        'result': True,
        'data': data
    })


def get_host(request,bk_biz_id):
    client = get_client_by_request(request)
    client.set_bk_api_ver('v2')
    res = client.cc.search_host({
        "page": {"start": 0, "limit": 10, "sort": "bk_host_id"},
        "ip": {
            "flag": "bk_host_innerip|bk_host_outerip",
            "exact": 1,
            "data": []
        },
        "condition": [
            {
                "bk_obj_id": "host",
                "fields": [
                ],
                "condition": []
            },
            {
                "bk_obj_id": "biz",
                "fields": [
                    "default",
                    "bk_biz_id",
                    "bk_biz_name",
                ],
                "condition": [
                    {
                        "field": "bk_biz_id",
                        "operator": "$eq",
                        "value": int(bk_biz_id)
                    }
                ]
            }
        ]
    })

    if res.get('result', False):
        bk_host_list = res.get('data').get('info')
    else:
        bk_host_list = []
        logger.error(u"请求主机列表失败：%s" % res.get('message'))

    bk_host_list = [
        {
            'bk_host_innerip': host['host']['bk_host_innerip'],
            'bk_host_name': host['host']['bk_host_name'],
            'bk_host_id': host['host']['bk_host_id'],
            'bk_os_type': host['host']['bk_os_type'],
            'bk_os_name': host['host']['bk_os_name'],
            'bk_cloud_id': host['host']['bk_cloud_id'][0]['bk_inst_id'],
            'bk_cloud_name': host['host']['bk_cloud_id'][0]['bk_inst_name'],
            'bk_set_name': ' '.join(map(lambda x: x['bk_set_name'], host['set'])[:1]),
            'bk_module_name': ' '.join(map(lambda x: x['bk_module_name'], host['module'])[:1]),
        }
        for host in bk_host_list
    ]
    return bk_host_list


def fast_execute_script(request):
    """快速执行脚本"""
    bk_biz_id = int(request.POST.get('bk_biz_id'))
    bk_host_innerip = request.POST.get('bk_host_innerip')
    bk_cloud_id = request.POST.get('bk_cloud_id')
    task_name = request.POST.get('task_type')
    script_param = request.POST.get('script_param')
    user_name = request.user.username
    celery_tasks.execute_task(bk_biz_id,bk_host_innerip ,bk_cloud_id,task_name,script_param,user_name)
    return render_json({
        'result': True,
        'data': '提交成功' })


def history(request):
    """
    操作历史
    """
    client = get_client_by_request(request)
    client.set_bk_api_ver('v2')

    # 查询业务
    res = client.cc.search_business()
    bk_biz_list = res.get('data').get('info')

    opt_list = OptLog.objects.order_by('-opt_at')
    return render_mako_context(request,
                               '/home_application/history.html', {
                                   'opt_list': opt_list,
                                   'bk_biz_list': bk_biz_list,
                               })




