# coding: utf-8
from django.db import models

class StatsType(models.Model):
    """Dane na temat statystyk i sposobów ich obliczania u szystkich bohaterów"""
    name = models.CharField(max_length=50)
    
class Package(models.Model):
    name = models.CharField(max_length=50)
    stats = models.ManyToManyField(StatsType)
