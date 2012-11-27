# coding: utf-8
from django.db import models
from decimal import Decimal

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
    
    def set_RPN(self):
        self.RPN = self._create_RPN()
    
    def _create_RPN(self):
        """Zmienia wzór zapisany w sposób standardowy w odwróconą polską notację"""
        right_to_left = ['^']
        operators_priority = {'':-5, '(': 0, ')': 0, '+': 5, '-': 5, '*': 10, '/': 10, '^': 15,
                              'random': 20, 'log': 20}
        
        input = self.text.replace(',', ') (')
        input = input.split();
        output = []
        operators = []
        for current in input:
            if not self._handle_operator(current, output, operators, right_to_left, 
                                          operators_priority):
                if not self._handle_number(current, output):
                    self._handle_reference(current, output)
        while operators:
            output.append(operators.pop())
        return output
    
    def _handle_operator(self, c, output, operators, right, priority):
        if not c in priority:
            return False  
        if c == '(':
            operators.append(c)
        elif c == ')':
            while operators[-1] != '(':
                output.append(operators.pop())
            if operators.pop() != '(':
                raise Exception("Missing (")
        else:
            cp = priority[c]
            if c in right:
                while operators and cp < priority[operators[-1]]:
                    output.append(operators.pop())
            else:
                while operators and cp <= priority[operators[-1]]:
                    output.append(operators.pop())
            operators.append(c)       
        return True
                
    
    def _handle_number(self, c, output):
        try:
            output.append(Decimal(c))
            return True
        except ValueError:
            return False
        
    def _handle_reference(self, c, output):
        output.append("ref")
    
    def _get_previous(self, operators):
        try:
            return operators[-1]
        except IndexError:
            return ''
                        
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
