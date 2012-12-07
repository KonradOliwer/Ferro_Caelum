# coding: utf-8
from django.db.models import signals
from django.db import models
from hero.dics import *
from hero.formula import *

class Stat(models.Model):
    """Współczynnik (np. bohatera, broni)"""
    name = models.ForeignKey(StatsType)
    additive = models.IntegerField(default=0)
    percent = models.PositiveIntegerField(default=0)
    base = models.IntegerField(default=1)
    formula = models.ForeignKey(Formula, null=True)
    
    def current_value(self):
        """Wartość faktyczna - wyliczona na podstaiwe trzech podtawowych parametrów (additive, percent, base)"""
        value = 0.01 * (100 + self.percent) * (self.base + self.additive)
        return value if value >= 0 else 0
    
    def __unicode__(self):
        return u'%s' % self.name.name
