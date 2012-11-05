# coding: utf-8
from engine.object import Object

__author__ = 'episage'

class Item(Object):
    """
    Abstract class.
    """

    def __init__(self, name, load=0, min_lvl=0, destroyable=True, tradable=True):
        super(Item, self).__init__(name)
        self.load = load
        self.min_lvl = min_lvl
        self.destroyable = destroyable
        self.tradable = tradable


class Items(object):
    def __init__(self, item, count=1, owner=None, effects=object):
        self.item = item
        self.count = count
        self.owner = owner
        self.effects = effects