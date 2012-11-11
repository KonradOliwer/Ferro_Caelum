# coding: utf-8
from django.db import models
from hero.talents import *

class StatsType(models.Model):
    """Słownik statystyk zapisany w bazie danych"""
    #długość jeszcze do przemyślenia
    name = models.CharField(max_length=50)

class AlgebraSignature(models.Model):
    """
    Element wzoru wyliczającego statystykę poboczną
     
    Może być wartością statystyki, stałą, operatorem lub znakiem pustym.
    """
    OPERATOR_CHOICES=(
                      (1, '+'),
                      (2, '-'),
                      (3, '*'),
                      (4, '/'),
                      (5, '^'),
                      (6, '-'),
                      (7, 'log'),
                      (9, 'funkcja wykładnicza'), 
                      (10, 'liczba z przedziału')
                      )
    
    stat_value = models.ForeignKey(StatsType, blank=True)
    constans = models.DecimalField(max_digits=9, decimal_places=3, blank=True)
    operation = models.IntegerField(choices=OPERATOR_CHOICES, blank=True)
    signature_right = models.ForeignKey('self', related_name='right',  blank=True)
    signature_left = models.ForeignKey('self', related_name='left', blank=True)

class Stat(models.Model):
    """
    Współczynnik bohatera
    
    Jego wartość bazowa jest wartością wprowadzaną, bądź jest obliczana na
    podstawie wozru.
    """
    type = models.ForeignKey(StatsType)
    additive_change = models.IntegerField(default=0)
    percent_change = models.PositiveIntegerField(default=0)
    base_value = models.IntegerField(default=1)
    formula = models.ManyToManyField(AlgebraSignature, blank=True)

    
# Warto przemyśleć przeniesienie klasy do osobnego pliku, dla zwiększenia 
# czytelności
class Fighter(models.Model):
    #Gracz chce móc rzucać czary zmieniające statystyki główne!
    stats = models.ManyToManyField(Stat)    
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

class BloodLine(models.Model):
    pass

class Profession(models.Model):
    pass

class Hero(Fighter):
    name = models.CharField(max_length=50)
    lvl = models.PositiveSmallIntegerField(default=1)
    exp = models.PositiveIntegerField(default=0)
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
    talents = models.ManyToManyField(Talent)