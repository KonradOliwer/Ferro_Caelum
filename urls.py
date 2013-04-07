from django.conf.urls import patterns, include, url
from django.views.static import *
from django.conf import settings
from registration.views import AccountRegistration,RegistrationOver
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from views import *

urlpatterns = patterns('',('^$', homepage),
    # Examples:
    # url(r'^$', 'Ferro_Caelum.views.home', name='home'),
    # url(r'^Ferro_Caelum/', include('Ferro_Caelum.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # Required to make static serving work
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^registration/', include('registration.urls')),
    url(r'^auth/', include('authorization.urls')),
    url(r'^hero_creator/', include('hero_creator.urls')),
    url(r'^mail/', include('message_system.urls')),
    url(r'^accounts/login/', TemplateView.as_view(template_name="login_required.html")),
)
