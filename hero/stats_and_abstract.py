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
    
class Condition(models.Model):
    OPERATOR_CHOICES = (
                      (1, '<'),
                      (2, '>'),
                      (3, '='),
                    )
    left = models.ForeignKey(StatsType, related_name='left')
    operator = models.PositiveSmallIntegerField(choices=OPERATOR_CHOICES, default=1)
    value = models.DecimalField(max_digits=6, decimal_places=3)
    right = models.ForeignKey(StatsType, related_name='right', blank=True)
    # if (left) (operator) value*(rigth or 1) 
    # np. if power > 0.05*hp
