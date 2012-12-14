# coding: utf-8
from django.db import models
from hero.formula import *

class StatsType(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    formula = models.ForeignKey(Formula, null=True, blank=True, default = None)
    
class BarsType(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
      
class Slot(models.Model):
    name = models.CharField(max_length=50)
    
class Package(models.Model):
    name = models.CharField(max_length=50)
    stats = models.ManyToManyField(StatsType)
    slots = models.ManyToManyField(Slot)
    
    def add_package(self, target):
        """Dodaje celowi pakiet"""
        target.packages.add(self)
        target.stats.add(self.stats)
        target.slots.add(self.slots)
    
    def __unicode__(self):
        return u'Pakiet: %s' % self.name