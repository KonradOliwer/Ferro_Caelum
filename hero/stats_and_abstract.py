# coding: utf-8
from django.db import models

class Package(models.Model):
    name = models.CharField(max_length=50)

class StatsType(models.Model):
    """Dane na temat statystyk i sposobów ich obliczania u szystkich bohaterów"""
    name = models.CharField(max_length=50)
    packages = models.ManyToManyField(Package)

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
    self_stat_value = models.BooleanField(default=True)
    constans = models.DecimalField(max_digits=9, decimal_places=3, blank=True)
    operation = models.IntegerField(choices=OPERATOR_CHOICES, blank=True)
    signature_right = models.ForeignKey('self', related_name='right', blank=True)
    signature_left = models.ForeignKey('self', related_name='left', blank=True)

class Stat(models.Model):
    """
    Współczynnik bohatera
    """
    type = models.ForeignKey(StatsType)
    additive_change = models.IntegerField(default=0)
    percent_change = models.PositiveIntegerField(default=0)
    base_value = models.IntegerField(default=1)
    formula = models.ForeignKey(AlgebraSignature, blank=True)