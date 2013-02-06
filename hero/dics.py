# coding: utf-8
from django.db import models
from hero.formula import *

class AtributType(models.Model):
    ATRIBUT_KIND_CHOICES = ((1, 'stat'),(2, 'bar'),)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    formula = models.ForeignKey(Formula, null=True, blank=True, default = None)
    kind = models.IntegerField(choices=ATRIBUT_KIND_CHOICES, default=1)
      
class Slot(models.Model):
    name = models.CharField(max_length=50)
    
class Package(models.Model):
    name = models.CharField(max_length=50)
    atributs = models.ManyToManyField(AtributType)
    slots = models.ManyToManyField(Slot)
    
    def __unicode__(self):
        return u'Pakiet: %s' % self.name