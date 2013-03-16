from django.conf.urls import patterns, url

urlpatterns = patterns('hero_creator.views',
    url(r'^$', 'start'),
    url(r'^start', 'start'),
    url(r'^blood_line/$', 'blood_line'),
    url(r'^profession/$', 'profession'),
    url(r'^confirm/$', 'confirm'),
    url(r'^end/$', 'end')
)
