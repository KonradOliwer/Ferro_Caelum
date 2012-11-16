# coding: utf-8
from django.db import models
from hero.stats_and_abstract import *

class EffectTypes(models.Model):
    name = models.CharField(max_length=50)

class Effect(models.Model):
    type = models.ForeignKey(EffectTypes, blank=True)
    INFINITE = 0
    dont_save_after_add = models.BooleanField(default=False)
    last = models.PositiveSmallIntegerField(default=INFINITE)
    stat = models.ForeignKey(StatsType)
    formula = models.ForeignKey(Formula)
    additive = models.BooleanField(default=True)

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


class Ability(models.Model):
    name = models.CharField(max_length=50)
    abilities_requirements = models.ManyToManyField('self', symmetrical=False)
    lvl_requirement = models.IntegerField(default=0)
    stats_abilities_requirements = models.ManyToManyField(Condition)
    
class Fighter(models.Model):
    name = models.CharField(max_length=50)
    lvl = models.PositiveSmallIntegerField(default=1)
    package = models.ManyToManyField(Package)
    stats = models.ManyToManyField(Stat)
    ability = models.ManyToManyField(Ability)    
    
class Slot(models.Model):
    name = models.CharField(max_length=50)
    
class Item(models.Model):
    type = models.ManyToManyField(Package)
    stats = models.ManyToManyField(Stat)
    abilities = models.ManyToManyField(Ability)
    used_slots = models.ManyToManyField(Slot)
    
class NPC(Fighter):
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
