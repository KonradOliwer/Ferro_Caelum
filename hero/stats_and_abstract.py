# coding: utf-8
from django.db import models

class StatsType(models.Model):
    """Dane na temat statystyk i sposobów ich obliczania u szystkich bohaterów"""
    name = models.CharField(max_length=50)
	
class Package(models.Model):
    name = models.CharField(max_length=50)
    stats = models.ManyToManyField(StatsType)

class Formula(models.Model):
    text = models.CharField(max_length=100)

class Stat(models.Model):
    """
    Współczynnik bohatera
    """
    type = models.ForeignKey(StatsType)
    additive_change = models.IntegerField(default=0)
    percent_change = models.PositiveIntegerField(default=0)
    base_value = models.IntegerField(default=1)
    formula = models.ForeignKey(Formula, blank=True)