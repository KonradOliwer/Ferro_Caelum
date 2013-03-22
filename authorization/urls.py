from django.conf.urls import patterns, url

urlpatterns = patterns('authorization.views',
    (r'^login/$', 'login_user'),
    (r'^logout/$', 'logout_user'),
)
