from django.conf.urls import patterns, url

urlpatterns = patterns('hero_creator.views',
    url(r'^$', 'index_blood_line')
)
