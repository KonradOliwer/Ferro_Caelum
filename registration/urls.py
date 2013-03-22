from django.conf.urls import patterns, url
from registration.views import AccountRegistration, RegistrationOver

urlpatterns = patterns('registration.views',
    ('^$', AccountRegistration),
    ('^ok/$', RegistrationOver.as_view()),
)