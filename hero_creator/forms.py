# coding: utf-8
#
#import datetime
#from django import forms
#from hero.models import *
#
#class CreateHero(forms.Form):
#    """Tworzenie bohatera przez użytkownika"""
#    name = forms.CharField(label=(u"Nazwa postaci"))
#    bloodline = forms.ModelMultipleChoiceField(label=(u"Linia krwii"), queryset=BloodLine.objects.all())
#    profession = forms.ModelMultipleChoiceField(label=(u"Typ wszczepu"), queryset=Profession.objects.all())
#    
#    class Meta:
#        model = Hero
#        exclude = ('stats', 'packages', 'slots')
#    
#    def save(self, user):
#        hero = Hero(name=name, bloodline=bloodline, profession=profession)
#        hero.save()
#        user.hero = hero
#        user.save()