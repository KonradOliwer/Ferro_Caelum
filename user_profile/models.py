# coding: utf-8
from django.db import models

from django.contrib.auth.models import User
from hero.models import Hero

class UserProfile(models.Model):
    hero = models.OneToOneField(Hero, null=True)
    user = models.ForeignKey(User, unique=True)
