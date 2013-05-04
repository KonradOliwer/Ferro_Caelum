# coding: utf-8
from django.db import models
from dics import *
from condition import Condition
from hero.attributes import *

def add_package(package, target):
    """Dodaje celowi pakiet i dostarcza wszystkich w nim zawartych elementów"""
    if not package in target.packages.all():
        target.packages.add(package)
        atributs = package.atributs.all()
        for atribut_name in atributs:
            if (atribut_name.kind == 1):
                stat = Stat.objects.create(name=atribut_name, owner=target)
            else:
                bar = Bar.objects.create(name=atribut_name, owner=target)
        slots = package.slots.all()
        for slot in slots:
            target.slots.add(slot)


class Effect(models.Model):
    atribut = models.ForeignKey(AtributType)
    additive = models.BooleanField(default=True)

class Ability(models.Model):
    name = models.CharField(max_length=50)
    abilities_requirements = models.ManyToManyField('self', symmetrical=False)
    lvl_requirement = models.IntegerField(default=0)
    stats_abilities_requirements = models.ManyToManyField(Condition)
    effects = models.ManyToManyField(Effect)
    
class Fighter(models.Model):
    packages = models.ManyToManyField(Package)
    name = models.CharField(max_length=50)
    lvl = models.PositiveSmallIntegerField(default=1)
    ability = models.ManyToManyField(Ability)
    
    def get_stats(self):
        return Stat.objects.filter(owner=self);
    
    def get_bars(self):
        return Bar.objects.filter(owner=self);
    
    def save(self, *args, **kwargs):
        super(Fighter, self).save(*args, **kwargs)
        package = Package.objects.get(name='wojownik')
        add_package(package, self)
         
    def setattr(self, name, kind, value_change):
        if hasattr(self, name):
            setattr(self, name, value_change)
        else:
            stat = Stat.objects.filter(owner=self.pk).get(name__name=name)
            if stat:
                setattr(stat, kind, value_change)
                stat.save()
                print(getattr(stat, kind))
            else:
                bar = Bar.objects.filter(owner=self.pk).get(name__name=name)
                setattr(bar, kind, value_change) 
                bar.save()  
    
    def getattr(self, name, kind=None):
        try:
            return getattr(self, name)
        except AttributeError:
            stat = Stat.objects.filter(owner=self.pk).get(name__name=name)
            if stat:
                if kind is None:
                    return stat.current_value()
                else:
                    return getattr(attribute, kind)
            else:
                bar = Bar.objects.filter(owner=self.pk).get(name__name=name)
                if kind is None:
                    return bar.current_value()
                else:
                    return getattr(attribute, kind)
            
    def recompute_attributes(self):
        """Aktualizuje wartości atrybutów obliczalnych (pole formula != null)"""
        stats = self.get_stats()
        for stat in stats:
            stat.recompute()
        bars = self.get_bars()
        for bar in bars:
            bar.recompute()
            
    def get_item_stat(self):
        return None
    
    def add_package(self, package):
        add_package(self)
    
    def __unicode__(self):
        return u'%s' % self.name
    
def fighter_recompute(instance, **kwargs):
    instance.recompute_attributes()
    
# models.signals.pre_save.connect(fighter_recompute, Fighter)
    
# class Item(models.Model):
#    name = models.CharField(max_length=50)
#    kind = models.ManyToManyField(Package)
#    stats = models.ManyToManyField(Stat)
#    abilities = models.ManyToManyField(Ability)
#    used_slots = models.ManyToManyField(Slot)
#            
#    def setattr(self, name, kind, value_change):
#        try:
#            setattr(self, name, value_change)
#        except AttributeError:
#            stat = self.stats.get(name__name=name)
#            setattr(stat, kind, value_change)   
#    
#    def getattr(self, name, kind=None):
#        try:
#            return getattr(self, name)
#        except AttributeError:
#            try:
#                stat = self.stats.get(name__name=name)
#            except Stat.DoesNotExist:
#                return None
#            if kind is None:
#                return stat.current_value()
#            else:
#                return getattr(stat, kind)    
    
class NPCFighter(Fighter):
    pass

class BloodLine(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

class Profession(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

class Hero(Fighter):
    exp = models.PositiveIntegerField(default=0)
    bloodline = models.ForeignKey(BloodLine)
    profession = models.ForeignKey(Profession)
    slots = models.ManyToManyField(Slot)
    can_figth = models.BooleanField(default=True)
    energy = models.PositiveIntegerField(default=10)
    current_energy = models.PositiveIntegerField(default=10)
#    equiped_items = models.ManyToManyField(Item, related_name='equiped')
#    items = models.ManyToManyField(Item, related_name='unequiped')
    
    def save(self, *args, **kwargs):
        super(Fighter, self).save(*args, **kwargs)
        package = Package.objects.get(name='bohater')
        add_package(package, self)
    
    def get_item_stat(self, item_name, stat_name, kind=None):
        try:
            item = self.equiped_items.get(kind__name=item_name)
        except Hero.DoesNotExists:
            try:
                item = self.equiped_items.get(name=item_name)
            except Hero.DoesNotExists:
                return None
        return item.getattr(stat_name, kind)
