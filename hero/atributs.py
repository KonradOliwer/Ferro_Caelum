# coding: utf-8
from django.db.models import signals
from django.db import models
from hero.dics import *
from hero.formula import *

class Atribut(models.Model):
    """Współczynnik obiektu (np. bohatera, broni)"""
    name = models.ForeignKey(AtributType)
    additive = models.IntegerField(default=0)
    percent = models.PositiveIntegerField(default=0)
    base = models.IntegerField(default=1)
    
    class Meta:
        abstract = True
        
    def current_value(self):
        """
        Wartość faktyczna - wyliczona na podstaiwe trzech podtawowych parametrów (additive,
        percent, base)
        """
        value = 0.01 * (100 + self.percent) * (self.base + self.additive)
        return value if value >= 0 else 0
    
    def __unicode__(self):
        return u'%s' % self.name.name

class Stat(Atribut):
    """
    Współczynnik względnie stała, modyfikowana jedynie przy awansie postaci, oraz przez efekty.
    """
    pass

class Bar(Atribut):
    """
    Współczynnik zmieniający się, o względnie stałej wartości maksymalnej, modyfikowanej
    jedynieprzy awansie postaci, oraz przez efekty.
    """
    current = models.PositiveIntegerField(default=10)
    regeneration = models.PositiveIntegerField(default=0)
    
    def current_max_value(self):
        """Wartość faktyczna - wyliczona na podstaiwe trzech podtawowych parametrów (additive, percent, base)"""
        return Atribut.current_value