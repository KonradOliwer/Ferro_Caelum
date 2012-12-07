# coding: utf-8
from django.test import TestCase
from hero.stats_and_abstract import *
from hero.models import *
import decimal 

class SimpleTest(TestCase):
    def setUp(self):
        self.bloodline = BloodLine.objects.create(name="Gangrel")
        self.profession = Profession.objects.create(name="Rybak")
        self.hero = Hero.objects.create(name=u"Stefań",
            bloodline=self.bloodline, profession=self.profession)
        self.hero.lvl = 2
        self.type1 = StatsType.objects.create(name="power")
        self.type2 = StatsType.objects.create(name="dexterity")
        self.type3 = StatsType.objects.create(name="web")
        self.type4 = StatsType.objects.create(name="inteligence")
        self.stat1 = Stat.objects.create(name=self.type1)
        self.stat2 = Stat.objects.create(name=self.type2)
        self.stat3 = Stat.objects.create(name=self.type3)
        self.stat4 = Stat.objects.create(name=self.type4)
        self.hero.stats.add(self.stat1, self.stat2, self.stat3, self.stat4)
        item = Item.objects.create(name='Gun')
        item.kind.create(name='range_wapon')
        range_damage = StatsType.objects.create(name='range_damage')
        range_damage_gun_stat = Stat.objects.create(name=range_damage)
        range_damage_gun_stat.base = 100
        range_damage_gun_stat.save()
        item.stats.add(range_damage_gun_stat)
        self.hero.equiped_items.add(item)
        self.hero.setattr('power', 'base', 10)
        self.hero.save()
                
        Formula.objects.create(text='5')
        Formula.objects.create(text='- 5')
        Formula.objects.create(text='- 5 * 3')
        Formula.objects.create(text='- 5 * ( 3 + 2 )')
        Formula.objects.create(text='- 5 ^ 2 * ( 3 + 2 )')
        Formula.objects.create(text='- 5 ^ ( 2 + 3 * 2 )')
        Formula.objects.create(text='1 + 2 / 4 + 2')
        Formula.objects.create(text='random ( 1 , 10 )')
        Formula.objects.create(text='5 + random ( 1 , 10 ) * 2')
        Formula.objects.create(text='log ( 2 , 4 )')
        Formula.objects.create(text='5 + log ( 2 , 4 ) * 2')
        Formula.objects.create(text='user.lvl')
        Formula.objects.create(text='2 * user.lvl ^ 2')
        Formula.objects.create(text='user.power')
        Formula.objects.create(text='target.range_wapon-range_damage')
        Formula.objects.create(text='5 * target.range_wapon-range_damage ^ 2')
        Formula.objects.create(text='5 * target.range_wapon-range_damage ^ 2')
        self.fo = Formula.objects.all()
        
    def test_formula_create_RPN(self):
        self.assertEqual(self.fo[0].RPN, [5])
        self.assertEqual(self.fo[1].RPN, [5, '-u'])
        self.assertEqual(self.fo[2].RPN, [5, '-u', 3, '*'])
        self.assertEqual(self.fo[3].RPN, [5, '-u', 3, 2, '+', '*'])
        self.assertEqual(self.fo[4].RPN, [5, '-u', 2, '^', 3, 2, '+', '*'])
        self.assertEqual(self.fo[5].RPN, [5, '-u', 2, 3, 2, '*', '+', '^'])
        self.assertEqual(self.fo[6].RPN, [1, 2, 4, '/', '+', 2, '+'])
        self.assertEqual(self.fo[7].RPN, [1, 10, 'random'])
        self.assertEqual(self.fo[8].RPN, [5, 1, 10, 'random', 2, '*', '+'])
        self.assertEqual(self.fo[9].RPN, [2, 4, 'log'])
        self.assertEqual(self.fo[10].RPN, [5, 2, 4, 'log', 2, '*', '+'])
        self.assertEqual(self.fo[11].RPN, [('user', None, 'lvl')])
        self.assertEqual(self.fo[12].RPN, [2, ('user', None, 'lvl'), 2, '^', '*'])
        self.assertEqual(self.fo[13].RPN, [('user', None, 'power')])
        self.assertEqual(self.fo[14].RPN, [('target', 'range_wapon', 'range_damage')])
        self.assertEqual(self.fo[15].RPN, [5, ('target', 'range_wapon', 'range_damage'), 2, '^', '*'])
    
    def test_formula_calculate(self):
        self.assertEqual(self.fo[0].calculate(self.hero, self.hero), 5)
        self.assertEqual(self.fo[1].calculate(self.hero, self.hero), -5)
        self.assertEqual(self.fo[2].calculate(self.hero, self.hero), -15)
        self.assertEqual(self.fo[3].calculate(self.hero, self.hero), -25)
        self.assertEqual(self.fo[4].calculate(self.hero, self.hero), 125)
        self.assertEqual(self.fo[5].calculate(self.hero, self.hero), 390625)
        self.assertEqual(self.fo[6].calculate(self.hero, self.hero), 3.5)
        self.assertTrue(self.calculate_random_test(7, 0, 11))
        self.assertTrue(self.calculate_random_test(8, 6, 26))
        self.assertEqual(self.fo[9].calculate(self.hero, self.hero), 2)
        self.assertEqual(self.fo[10].calculate(self.hero, self.hero), 9)
        self.assertEqual(self.fo[11].calculate(self.hero, self.hero), 2)
        self.assertEqual(self.fo[12].calculate(self.hero, self.hero), 8)
        self.assertEqual(self.fo[13].calculate(self.hero, self.hero), 10)
        self.assertEqual(self.fo[14].calculate(self.hero, self.hero), 100)
        self.assertEqual(self.fo[15].calculate(self.hero, self.hero), 50000)
        
    def calculate_random_test(self, n, min, max):
        for i in range(1, 100):
            t = self.fo[n].calculate(self.hero, self.hero)
            if t < min or t > max:
                return False
        else:
            return True
