from django.conf.urls import patterns, include, url
from django.views.static import *
from django.conf import settings
from registration.views import AccountRegistration,RegistrationOver

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from views import Homepage

urlpatterns = patterns('',('^$', Homepage.as_view()),
    # Examples:
    # url(r'^$', 'Ferro_Caelum.views.home', name='home'),
    # url(r'^Ferro_Caelum/', include('Ferro_Caelum.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # Required to make static serving work
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    ('^registration/$', AccountRegistration),
    ('^registration_ok/$', RegistrationOver.as_view()),
    (r'^login/$', 'authorization.views.login_user'),
    (r'^logout/$', 'authorization.views.logout_user'),
    #mejle
    (r'^inbox/$', 'message_system.views.inbox'),
    (r'^outbox/$', 'message_system.views.outbox'),
     url(r'^mail_view/(?P<message_id>[\d]+)/$', 'message_system.views.view', name='messages_detail'),
    (r'^new_mail/$', 'message_system.views.compose'),

)
