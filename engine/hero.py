# coding: utf-8
from engine.object import Object

__author__ = 'episage'

class Creature(Object):
    """
    Abstract class.
    """

    def __init__(self, name, max_hp=10):
        super(Creature, self).__init__(name)
        self.max_hp = self.hp = max_hp


class Owner(Creature):
    """
    Abstract class.
    You always can wear an item. No matter who you are.
    """

    def __init__(self, name, max_load=100):
        super(Owner, self).__init__(name)
        self.load = 0
        self.max_load = max_load


class Fighter(Owner):
    """
    Abstract class.
    Contains minimal fields to fight.
    """

    def __init__(self, name, max_hp=10, max_ap=10,):
        super(Fighter, self).__init__(name, max_hp)
        self.max_ap = self.ap = max_ap
        
    def start_batllemode(self):
        pass


#===============================================================================
# 
#===============================================================================
class Hero(Fighter):
    def __init__(self, name, blood_line, profession, lvl=1, exp=0, energy=20, 
            power=10, resistance=10, dexterity=10, perception=10, 
            intelligence=10, web=10, artifice=10):
        super(Object, self).__init__(name)
        #TODO zastanowić się nad organizacją statystyk
        #=======================================================================
        # self.lvl = lvl
        # self.exp = exp
        # self.blood_line = blood_line
        # self.profession = profession
        # self.energy = energy
        # self.power = power #moc
        # self.resistance = resistance #wytrzymałość
        # self.dexterity = dexterity #sprawność
        # self.perception = perception #percepcja
        # self.intelligence = intelligence #inteligencja
        # self.web = web #sieć
        # self.artifice = artifice #spryt
        #=======================================================================
        
        def start_batllemode(self):
            pass