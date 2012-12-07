# coding: utf-8
from django.db.models import signals
from django.db import models
from dics import StatsType
    
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