#!usr/bin/env python
# encoding=utf-8

from django.conf.urls.defaults import *
from rclickatell import views


urlpatterns = patterns('',
    url(r'^clickatell/test-message/$', views.test,
        name='clickatell-test-message'),
    url(r'^clickatell/status-callback/$', views.status_callback,
        name='clickatell-callback'),
)
