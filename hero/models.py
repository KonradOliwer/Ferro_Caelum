# coding: utf-8
from django.db import models
from hero.stats_and_abstract import *

class EffectTypes(models.Model):
    name = models.CharField(max_length=50)

class Effect(models.Model):
    INFINITE = 0
    
    last = models.PositiveSmallIntegerField(defult=INFINITE)
    type = models.ForeignKey(EffectTypes, blank=True)
    stat = models.ForeignKey(StatsType)
    formula = models.ForeignKey(AlgebraSignature)
    additive = models.BooleanField(defult=True)

class Action(models.Model):
    SELF = 1
    ENEMY = 2
    ALLY = 3
    
    TARGET_CHOICES=(
        (SELF, 'osobisty'),
        (ENEMY, 'przeciwnik'),
        (ALLY, 'sojusznik'),
        )
    
    name = models.CharField(max_length=50)
    auto_activation = models.BooleanField(defult=False)
    only_battle = models.BooleanField(defult=True)
    effects = models.ManyToManyField(Effect)
    target = models.PositiveSmallIntegerField(choices=TARGET_CHOICES, defult=SELF)


class Ability(models.Model):
    name = models.CharField(max_length=50)
    action = models.ManyToManyField(Action, blank=True)
    #===========================================================================
    # Tutaj skończyłem pracę
    #===========================================================================
    
class Fighter(models.Model):
    stats = models.ManyToManyField(Stat)
    ability = models.ManyToManyField(Ability)    
    
class Slot(models.Model):
    name = models.CharField(max_length=50)
    
class Item(models.Model):
    type = models.ManyToManyField(Package)
    stats = models.ManyToManyField(Stat)
    abilities = models.ManyToManyField(Ability, blank=True)
    used_slots = models.ManyToManyField(Slot, blank=True)
    
class Enemy(Fighter):
    pass

class BloodLine(models.Model):
    name = models.CharField(max_length=50)

class Profession(models.Model):
    name = models.CharField(max_length=50)

class Hero(Fighter):
    name = models.CharField(max_length=50)
    lvl = models.PositiveSmallIntegerField(default=1)
    exp = models.PositiveIntegerField(default=0)
    bloodline = models.ForeignKey(BloodLine)
    profession = models.ForeignKey(Profession)
    slots = models.ManyToManyField(Slot)
    can_figth = models.BooleanField(defult=True)
