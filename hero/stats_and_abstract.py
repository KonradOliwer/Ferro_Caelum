# coding: utf-8
from django.db import models

class StatsType(models.Model):
    """Dane na temat statystyk i sposobów ich obliczania u szystkich bohaterów"""
    name = models.CharField(max_length=50)
	
class Package(models.Model):
    name = models.CharField(max_length=50)
    stats = models.ManyToManyField(StatsType)

class Formula(models.Model):
    text = models.CharField(max_length=100)
    
    def get_value(self, user, target):
        if not hasattr(self, 'f'):
            self.s = self._create_stack()
            self.f = self._create_formula()
        return self.f(user, target)
    
    def _create_stack(self):
        stack = []
        return stack
    
    def _create_formula(self):
        return lambda user, target: self.s
        

class Stat(models.Model):
    """
    Współczynnik bohatera
    """
    name = models.ForeignKey(StatsType)
    additive = models.IntegerField(default=0)
    percent = models.PositiveIntegerField(default=0)
    base = models.IntegerField(default=1)
    formula = models.ForeignKey(Formula, null=True)
    
    def current_value(self):
        value = 0.01 * (100 + self.percent) * (self.base + self.additive)
        return value if value >= 0 else 0
    
    def __unicode__(self):
        return u'%s' % self.name.name
    
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
