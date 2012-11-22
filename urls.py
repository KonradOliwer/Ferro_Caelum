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
)
