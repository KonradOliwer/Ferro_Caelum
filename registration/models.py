# coding: utf-8
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from user_profile.models import UserProfile


class RegistrationForm(forms.Form):
    username    = forms.CharField(label = (u'Nazwa użytkownika'))
    email       = forms.EmailField(label=(u'Adres Email'))
    password    = forms.CharField(label=(u'Hasło'), widget=forms.PasswordInput(render_value=False))
    password_re = forms.CharField(label=(u'Powtórz hasło'),widget=forms.PasswordInput(render_value=False))
    #age
    #sex
    class Meta:
        model = UserProfile
        exclude = ('user', 'hero')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username = username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Nazwa użytkownika zajęta. Wybierz inną.")

    def clean(self):
        password = self.cleaned_data.get('password', None)
        password_re = self.cleaned_data.get('password_re', None)
        if password != password_re:
            raise forms.ValidationError("Haslo niezgodne z polem do jego konfirmacji")
        return self.cleaned_data