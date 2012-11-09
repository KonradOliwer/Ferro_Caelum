# coding: utf-8
from django.db import models

class StatsType(models.Model):
    """Słownik statystyk zapisany w bazie danych"""
    #długość jeszcze do przemyślenia
    name = models.CharField(max=50)

class Stat(models.Model):
    type = models.ForeignKey(StatsType)
    additive_change = models.IntegerField(defult=0)
    percent_change = models.PositiveIntegerField(defult=0)
    base_value = models.IntegerField(defult=1)

class Formula(models.Model):
    """Element wzoru wyliczającego statystykę poboczną"""
    pass

class SubstatsType(StatsType):
    """Słownik statystyk pobocznych zapisany w bazie danych"""
    formula = models.ManyToManyField(Formula)

class Substat(Stat): 
    """Współczynnik obliczany na podstawie wartości statystyk głównych"""
    type = models.ForeignKey(StatsType)

# Warto przemyśleć przeniesienie klasy do osobnego pliku, dla zwiększenia czytelności
class Fighter(models.Model):
    #Gracz chce móc rzucać czary zmieniające statystyki główne!
    stats = models.ManyToManyField(Stat) 
    common_stats = models.ManyToManyField(Substat)
    
    #===========================================================================
    # Propozycje metod; Do przemyślenia przy realizacji systemu walki
    # 
    # 
    # def melee_atack(self, enemy):
    #    pass
    # 
    # def range_atack(self, enemy):
    #    pass
    # 
    # def move(self):
    #    pass
    # 
    # def activate_program(self, target):
    #    # Wirus albo program wspierajćy
    #    # UWAGA! Konflikt nazw, warto znaleźć zamiennik dla 'program'
    #    pass
    # 
    # def activate_field(self, enemy):
    #    pass
    # 
    # def web_attack(self, enemy):
    #    pass
    #===========================================================================

class NPCFighter(Fighter):
    pass

class Hero(Fighter):
    name = models.CharField(max=50)
    lvl = models.PositiveSmallIntegerField(defult=1)
    exp = models.PositiveIntegerField(defult=0)
    bloodline = models.ForeignKey('BloodLine')
    profession = models.ForeignKey('Profession')
    #===========================================================================
    # Nazwa Talent podobno nie najlepsza, są jakieś inne propozycje nie idąca w
    # konflikcie z Ability? 
    #===========================================================================
    #===========================================================================
    # zdanie przerzucam, żeby nie mieć długości lini
    # kodu dłuższej niż 80 znaków rekomendowane standardy 80, 100, 120)
    # nie wiem tylko dlaczego aptana Ctrl+$ generuje długość ramki na 81 -.-
    #===========================================================================
    talents = models.ManyToManyField('Talent')