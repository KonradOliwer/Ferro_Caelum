# coding: utf-8
from django.db.models import signals
from django.db import models
from hero.dics import *
import decimal 
import random
import math


#===============================================================================
# Sherlock Holmes and Dr Watson were going camping. They pitched their tent under the stars and
# went to sleep. Sometime in the middle of the night Holmes woke Watson up and said: "Watson, look
# up at the sky, and tell me what you see." Watson replied: "I see millions and millions of stars."
# Holmes said: "And what do you deduce from that?" Watson replied: "Well, if there are millions of
# stars, and if even a few of those have planets, it’s quite likely there are some planets like
# Earth out there. And if there are a few planets like Earth out there, there might also be life."
# And Holmes said: "Watson, you idiot, it means that somebody stole our tent."
#===============================================================================

class Formula(models.Model):
    """Zapis wzorów w systemie"""
    text = models.CharField(max_length=100)
    _operators = {#'nazwa': (priorytet, funkcja)
                  '': (-5,), '(': (0,),
                   ')': (0,),       
                  '+': (5, lambda a, b: a + b),
                  '*': (10, lambda a, b: a * b),
                  '/': (10, lambda a, b: a / b), 
                  '^': (15, lambda a, b: decimal.Decimal(math.pow(a, b))),
                  '-u': (17, lambda a:-a),
                  'random': (20, lambda a, b: random.randint(int(a), int(b))),
                  'log': (20, lambda base, a: decimal.Decimal(math.log(a, base)))}
    
    def __init__(self, *args, **kwargs):
        super(Formula, self).__init__(*args, **kwargs)
        self.create_RPN()
    
    def calculate(self, user, target):
        """Wykorzystuje wzór do obliczenia wartości dla zadanego celu i osoby aktywującej"""
        stack = []
        r = 0
        for token in self.RPN:
            result = self._hendle_operator(token, stack, user, target)
            if not result:
                stack.append(self._get_value(token, user, target))
        return stack[0]
    
    def create_RPN(self):
        """Zmienia wzór zapisany w sposób standardowy w odwróconą polską notację"""     
        signals.post_init.send(sender=self.__class__, instance=self)
        right_to_left = ['^', '-u']
        
        input = self.text.replace(',', ') (')
        if input[0] == '-':
            input = '-u' + input[1:]
        input = input.split();
        output = []
        operators_stack = []
        for current in input:
            if not self._add_operator(current, output, operators_stack, right_to_left):
                if not self._add_number(current, output):
                    if not self._add_reference(current, output):
                        raise Exception(u'Incorect value in formula')
        while operators_stack:
            output.append(operators_stack.pop())
        self.RPN = output
    
    def _get_priority(self, operator):
        """Dostarcza priorytet wskazanego operatora"""
        return self._operators[operator][0]
    
    def _get_function(self, operator):
        """Dostarcza funckję rperezentowaną przez wskazany operator"""
        return self._operators[operator][1]
    
    def _hendle_operator(self, token, stack, user, target):
        """Obsługuje elementy będące operatorami"""
        if not token in self._operators:
            return False
        arg = self._get_value(stack.pop(), user, target)
        if token == '-u':
            stack.append(self._get_function(token)(arg))
        else:
            arg1 = self._get_value(stack.pop(), user, target)
            stack.append(self._get_function(token)(arg1, arg))
        return True
                                               
    def _get_value(self, token, u, t):
        """Pobiera wartość pola z bazy danych"""
        try:
            token + 1
            return token
        except TypeError:
            target, item, stat = token
            if item is None:
                if target=='target':
                    return decimal.Decimal(getattr(t, 'getattr')(stat) or 0)
                else:
                    return decimal.Decimal(getattr(u, 'getattr')(stat) or 0)
            else:
                if target=='target':
                    return decimal.Decimal(getattr(t, 'get_item_stat')(item, stat) or 0)
                else:
                    return decimal.Decimal(getattr(u, 'get_item_stat')(item, stat) or 0)
        
    def _add_operator(self, c, output, operators_stack, right):
        """Obsługuje dodawnie operatorów do RPN"""
        if not c in self._operators:
            return False  
        if c == '(':
            operators_stack.append(c)
        elif c == ')':
            while operators_stack[-1] != '(':
                output.append(operators_stack.pop())
            if operators_stack.pop() != '(':
                raise Exception(u'Missing (')
        else:
            cp = self._get_priority(c)
            if c in right:
                while operators_stack and cp < self._get_priority(operators_stack[-1]):
                    output.append(operators_stack.pop())
            else:
                while operators_stack and cp <= self._get_priority(operators_stack[-1]):
                    output.append(operators_stack.pop())
            operators_stack.append(c)       
        return True                
    
    def _add_number(self, c, output):
        """Obsługuje dodawanie liczb do RPN"""
        try:
            output.append(decimal.Decimal(c))
            return True
        except (ValueError, decimal.InvalidOperation):
            return False
        
    def _add_reference(self, c, output):
        """Obsługuje dodawanie odwołania do pola w bazie danych do RPN"""
        try:
            target, atribute = c.split('.')
            try:
                item, stat = atribute.split('-') 
            except ValueError:
                item = None
                stat = atribute
            output.append((target, item, stat))
            return True
        except ValueError:
            return False
    
    def _get_previous(self, operators_stack):
        try:
            return operators_stack[-1]
        except IndexError:
            return ''
    
    