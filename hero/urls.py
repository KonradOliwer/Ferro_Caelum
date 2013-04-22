from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from views import *

urlpatterns = patterns('',
    url(r'^$', stats_main)
)
