# coding=utf-8
from django.db import models

from django.contrib.auth.models import User
from hero.models import Hero

class UserProfile(models.Model):
   # hero = models.ForeignKey(Hero)         # v dopóki hero nie ma tworzenia
    hero = models.CharField(max_length=50)  # tymczasowo....
    user = models.ForeignKey(User, unique=True)
