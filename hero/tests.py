# coding: utf-8
from django.test import TestCase
from hero.stats_and_abstract import *
from hero.models import *

class SimpleTest(TestCase):
    def setUp(self):
        self.bloodline = BloodLine.objects.create(name="Gangrel")
        self.profession = Profession.objects.create(name="Rybak")
        self.hero = Hero.objects.create(name=u"Stefań",
            bloodline=self.bloodline, profession=self.profession)
        self.type1 = StatsType.objects.create(name="power")
        self.type2 = StatsType.objects.create(name="dexterity")
        self.type3 = StatsType.objects.create(name="web")
        self.type4 = StatsType.objects.create(name="inteligence")
        self.stat1 = Stat.objects.create(name=self.type1)
        self.stat2 = Stat.objects.create(name=self.type2)
        self.stat3 = Stat.objects.create(name=self.type3)
        self.stat4 = Stat.objects.create(name=self.type4)
        self.hero.stats.add(self.stat1, self.stat2, self.stat3, self.stat4)
        self.formula = Formula.objects.create()
        
    def test_python_option(self):
        self.formula = Formula(text = '5 + 2 * ( 1 + 2 ^ 2 - random ( 0 , 3 ) ^ 9 ) ^ 2 ^ 3 + 5')
        self.formula.save()
        self.formula.set_RPN()
        print self.formula.text
        print self.formula.RPN