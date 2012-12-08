# coding=utf-8
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class MsgManager(models.Manager):
    """
    Manager do klasy Message
    """

    def inbox_for(self, user):
        """
        Zwraca wszystkie wiadomości otrzymane przez usera
        """
        return self.filter(receiver=user)

    def outbox_for(self, user):
        """
        Zwraca wszystkie wiadomości wysłane przez usera
        """
        return self.filter(author=user)

class Message(models.Model):
    """
    Reprezentuje pojedynczą wiadomość
    """
    author = models.ForeignKey(User,related_name='author')
    receiver = models.ForeignKey(User,related_name='received')
    subject = models.CharField(max_length=50)
    text = models.CharField(max_length=1000)
    date_sent=models.DateTimeField()
    read = models.BooleanField(default=False)

    objects=MsgManager()

    def __unicode__(self):
        return self.subject

    def mark_as_read(self):
        self.read=True

    def send(self):
        super(Message, self).save()

    def get_absolute_url(self):
            return ('messages_detail', [self.id])
    get_absolute_url = models.permalink(get_absolute_url)

def inbox_count_for(user):
    """
    Zwraca ilość nieprzeczytanych wiadomości
    """
    return Message.objects.filter(receiver=user, read=False).count()