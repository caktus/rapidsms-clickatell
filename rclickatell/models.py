import datetime

from django.db import models

from rapidsms.models import Connection


class Message(models.Model):
    connection = models.ForeignKey(Connection,
                                   related_name='clickatel_messages')
    date = models.DateTimeField()
    body = models.CharField(max_length=512)
    api_message_id = models.CharField('API Message ID', max_length=64,
                                      blank=True)

    def save(self, **kwargs):
        if not self.date:
            self.date = datetime.datetime.now()
        return super(Message, self).save(**kwargs)
    
    def __unicode__(self):
        return "%s..." % self.body[:16]


class MessageStatus(models.Model):

    STATUS_DESC = {
        '001': 'Message unknown',
        '002': 'Message queued',
        '003': 'Delivered to gateway',
        '004': 'Received by recipient',
        '005': 'Error with message',
        '006': 'User cancelled message delivery',
        '007': 'Error delivering message',
        '008': 'OK',
        '009': 'Routing error',
        '010': 'Message expired',
        '011': 'Message queued for later delivery',
        '012': 'Out of credit',
    }
    STATUS_DETAIL = {
        '001': 'The message ID is incorrect or reporting is delayed.',
        '002': 'The message could not be delivered and has been queued for attempted redelivery.',
        '003': 'Delivered to the upstream gateway or network (delivered to the recipient).',
        '004': 'Confirmation of receipt on the handset of the recipient.',
        '005': 'There was an error with the message, probably caused by the content of the message itself.',
        '006': 'The message was terminated by a user (stop delivery message command) or by our staff.',
        '007': 'An error occurred delivering the message to the handset.',
        '008': 'Message received by gateway.',
        '009': 'The routing gateway or network has had an error routing the message.',
        '010': 'Message has expired before we were able to deliver it to the upstream gateway. No charge applies.',
        '011': 'Message has been queued at the gateway for delivery at a later time (delayed delivery).',
        '012': 'The message cannot be delivered due to a lack of funds in your account. Please re-purchase credits.',
    }

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
