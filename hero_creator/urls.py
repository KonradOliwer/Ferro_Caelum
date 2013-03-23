from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from hero_creator.views import *

urlpatterns = patterns('',
    url(r'^$', start),
    url(r'^start', start),
    url(r'^blood_line/$', blood_line),
    url(r'^profession/$', profession),
    url(r'^name/$', name),
    url(r'^confirm/$', confirm),
    url(r'^end/$', end)
)
