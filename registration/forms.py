import datetime
from django import forms
from hero.models import *

class CreateHero(forms.Form):
    """Tworzenie bohatera przez użytkownika"""
    h_name = forms.CharField(label=(u"Nazwa postaci"))
    h_bloodline = forms.ModelMultipleChoiceField(label=(u"Linia krwii"), queryset=BloodLine.objects.all())
    h_profession = forms.ModelMultipleChoiceField(label=(u"Typ wszczepu"), queryset=Profession.objects.all())
    
    class Meta:
        model = Hero
        exclude = ('stats', 'packages', 'slots')
    
    def save(self, user):
        hero = Hero(name=h_name, bloodline=h_bloodline, profession=h_profession)
#        hero.save()
#        user.