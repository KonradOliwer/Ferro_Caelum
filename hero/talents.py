# coding: utf-8
from django.db import models

class Talent(models.Model):
    name = models.CharField(max_length=50)