__author__ = 'Tyrael'
from django.db import models
from hero.models import Hero

class Battle(models.Model):
    date = models.DateTimeField
    sides = models.ManyToManyField(Hero)
    winner = models.OneToOneField(Hero)
    logs = models.ForeignKey(Logs)


class Logs(models.Model):
    #tu sie jakos musi zawrzec lista. Pisze offline, wiec nie wiem jak.
    battle = models.ForeignKey(Battle)