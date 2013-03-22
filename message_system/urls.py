from django.conf.urls import patterns, url

urlpatterns = patterns('message_system.views',
    (r'^inbox/$', 'inbox'),
    (r'^outbox/$', 'outbox'),
    url(r'^mail_view/(?P<message_id>[\d]+)/$', 'view', name='messages_detail'),
    (r'^new_mail/$', 'compose')
)