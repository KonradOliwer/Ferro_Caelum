# coding: utf-8
from django.db.models import signals
from django.db import models
from hero.dics import *
from hero.formula import *

class Bar(models.Model):
    name = models.ForeignKey(BarsType)
    current = models.IntegerField(default=0)
    base_max = models.IntegerField(default=10)
    additive_max = models.IntegerField(default=0)
    percent_max = models.PositiveIntegerField(default=0)
    
    def current_max_value(self):
        """Wartość faktyczna - wyliczona na podstaiwe trzech podtawowych parametrów (additive, percent, base)"""
        value = 0.01 * (100 + self.percent_max) * (self.base_max + self.additive_max)
        return value if value >= 0 else 0