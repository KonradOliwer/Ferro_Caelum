# coding=utf-8
import datetime
from django import forms
from django.contrib.auth.models import User
from mail.models import Message

class ComposeForm(forms.Form):
    """
    A simple default form for private messages.
    """
    recipient =forms.CharField(label=(u"Do"))
    subject = forms.CharField(label=(u"Temat"))
    body = forms.CharField(label=(u"Treść"),
        widget=forms.Textarea(attrs={'rows': '12', 'cols':'55'}))


    def clean_recipient(self):
        username = self.cleaned_data['recipient']
        try:
            User.objects.get(username = username)
        except User.DoesNotExist:
            raise forms.ValidationError("Brak użytkownika o podanym nicku.")
        return username

    def save(self, sender, parent_msg=None):
        recipient = User.objects.get(username=self.cleaned_data['recipient'])
        subject = self.cleaned_data['subject']
        body = self.cleaned_data['body']
        msg = Message(
                author = sender,
                receiver = recipient,
                subject = subject,
                text = body,
                date_sent=datetime.datetime.now()
            )
        msg.save()

