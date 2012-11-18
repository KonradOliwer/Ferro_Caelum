# coding: utf-8
from django.db import models
from hero.stats_and_abstract import *

class Effect(models.Model):
    stat = models.ForeignKey(StatsType)
    additive = models.BooleanField(default=True)

class Ability(models.Model):
    name = models.CharField(max_length=50)
    abilities_requirements = models.ManyToManyField('self', symmetrical=False)
    lvl_requirement = models.IntegerField(default=0)
    stats_abilities_requirements = models.ManyToManyField(Condition)
    effects = models.ManyToManyField(Effect)
    
class Fighter(models.Model):
    name = models.CharField(max_length=50)
    lvl = models.PositiveSmallIntegerField(default=1)
    package = models.ManyToManyField(Package)
    stats = models.ManyToManyField(Stat)
    ability = models.ManyToManyField(Ability)  
         
    def setattr(self, name, kind, value_change):
        try:
            setattr(self, name, value_change)
        except AttributeError:
            setattr(stat, kind, value_change)   
    
    def getattr(self, name, kind=None):
        try:
            return getattr(self, name)
        except AttributeError:
            stat = self.stats.get(name__name=name)
            if kind is None:
                return stat.current_value()
            else:
                return getattr(stat, kind)   
    
    def __unicode__(self):
        return u'%s' % self.name 
    
class Slot(models.Model):
    name = models.CharField(max_length=50)
    
class Item(models.Model):
    kind = models.ManyToManyField(Package)
    stats = models.ManyToManyField(Stat)
    abilities = models.ManyToManyField(Ability)
    used_slots = models.ManyToManyField(Slot)
    
class NPCFighter(Fighter):
    pass

class BloodLine(models.Model):
    name = models.CharField(max_length=50)

class Profession(models.Model):
    name = models.CharField(max_length=50)

class Hero(Fighter):
    exp = models.PositiveIntegerField(default=0)
    bloodline = models.ForeignKey(BloodLine)
    profession = models.ForeignKey(Profession)
    slots = models.ManyToManyField(Slot)
    can_figth = models.BooleanField(default=True)
    energy = models.PositiveIntegerField(default=10)
    current_energy = models.PositiveIntegerField(default=10)