# coding: utf-8
from django.db import models
from hero.dics import *
from hero.formula import *

class Attribute(models.Model):
    """Współczynnik postaci mogącej walczyć"""
    name = models.ForeignKey(AtributType)
    additive = models.IntegerField(default=0)
    percent = models.PositiveIntegerField(default=0)
    base = models.IntegerField(default=1)
    owner = models.ForeignKey('Fighter')
    
    class Meta:
        abstract = True
        
    def current_value(self):
        """
        Wartość faktyczna - wyliczona na podstaiwe trzech podtawowych parametrów (additive,
        percent, base)
        """
        value = 0.01 * (100 + self.percent) * (self.base + self.additive)
        return value if value >= 0 else 0
    
    def recompute(self):
        """Aktualizuje wartość atrybutu wyliczanego z formuły"""
        if self.name.formula:
            formula.calculate()
            
    def save(self, *args, **kwargs):
        self.owner.recompute_attributes()
        super(Attribute, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return u'%s%d: %d' % (self.name.name, self.pk, self.current_value())

class Stat(Attribute):
    """
    Współczynnik względnie stała, modyfikowana jedynie przy awansie postaci, oraz przez efekty.
    """
    pass

class Bar(Attribute):
    """
    Współczynnik zmieniający się, o względnie stałej wartości maksymalnej, modyfikowanej
    jedynieprzy awansie postaci, oraz przez efekty.
    """
    current = models.PositiveIntegerField(default=10)
    regeneration = models.PositiveIntegerField(default=0)
    
    def current_max_value(self):
        """Wartość faktyczna - wyliczona na podstaiwe trzech podtawowych parametrów (additive, percent, base)"""
        return super(Attribute, self).current_value()