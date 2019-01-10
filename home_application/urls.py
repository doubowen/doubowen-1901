# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^test/$', 'test'),
    (r'^api/get_hosts/$', 'get_hosts'),
    (r'^api/fast_execute_script/$', 'fast_execute_script'),
    (r'^history/$', 'history'),
    (r'^home/$', 'home'),
)
