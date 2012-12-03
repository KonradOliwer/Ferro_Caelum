# coding: utf-8
from django.db.models import signals
from django.db import models
import decimal 
import random
import math

class StatsType(models.Model):
    """Dane na temat statystyk i sposobów ich obliczania u szystkich bohaterów"""
    name = models.CharField(max_length=50)
	
class Package(models.Model):
    name = models.CharField(max_length=50)
    stats = models.ManyToManyField(StatsType)

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
    text = models.CharField(max_length=100)
    operators = {'': (-5,), '(': (0,), ')': (0,), '+': (5, lambda a, b: a + b),
                          '-': (5, lambda a, b: a - b), '*': (10, lambda a, b: a * b),
                          '/': (10, lambda a, b: a / b), 
                          '^': (15, lambda a, b: decimal.Decimal(math.pow(a, b))),
                          '-u': (17, lambda a:-a),
                          'random': (20, lambda a, b: random.randint(int(a), int(b))),
                          'log': (20, lambda base, a: math.log(a, base))}
    
    def __init__(self, *args, **kwargs):
        super(Formula, self).__init__(*args, **kwargs)
        self.create_RPN()
    
    def calculate(self, user, target):
        """Wykorzystuje wzór do obliczenia wartości dla zadanego celu i osoby aktywującej"""
        stack = []
        r = 0
        for token in self.RPN:
            result = self._hendle_operator(token, stack)
            if not result:
                stack.append(token)
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
        return self.operators[operator][0]
    
    def _get_function(self, operator):
        return self.operators[operator][1]
    
    def _hendle_operator(self, token, stack):
        if not token in self.operators:
            return False
        arg = self._get_value(stack)
        if token == '-u':
            stack.append(self._get_function(token)(arg))
        else:
            arg1 = self._get_value(stack)
            stack.append(self._get_function(token)(arg1, arg))
        return True
                                               
    def _get_value(self, stack):
        token = stack.pop()
        if token is decimal.Decimal or int:
            return token
        else:
            target, item, stat = token
            if item is None:
                return getattr(target, 'getattr')(stat)
            else:
                raise Exception(u"Not yet supported")
        
    def _add_operator(self, c, output, operators_stack, right):
        if not c in self.operators:
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
        try:
            output.append(decimal.Decimal(c))
            return True
        except (ValueError, decimal.InvalidOperation):
            return False
        
    def _add_reference(self, c, output):
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
