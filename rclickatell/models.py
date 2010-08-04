import datetime

from django.db import models

from rapidsms.models import Connection


class Message(models.Model):
    connection = models.ForeignKey(Connection)
    date = models.DateTimeField()
    body = models.CharField(max_length=512)
    api_message_id = models.CharField('API Message ID', max_length=64,
                                      blank=True)

    def save(self, **kwargs):
        if not self.date:
            self.date = datetime.datetime.now()
        return super(Message, self).save(**kwargs)


class MessageStatus(models.Model):
    message = models.ForeignKey(Message, related_name='statuses')
    ip_address = models.IPAddressField('IP Address')
    date = models.DateTimeField()
    sender = models.CharField(max_length=16)
    recipient = models.CharField(max_length=16)
    status = models.CharField(max_length=16)
    api_id = models.CharField('API ID', max_length=64)
    charge = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Message statuses'
