from django.contrib import admin
from hero.models import Hero
from hero.attributes import *

admin.site.register(Hero)
admin.site.register(Bar)
admin.site.register(Stat)