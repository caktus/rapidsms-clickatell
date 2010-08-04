import urllib
import urllib2
import urlparse
import pprint
import datetime
import time
import re

from django.http import QueryDict
from django.db import DatabaseError

from rapidsms.log.mixin import LoggerMixin
from rapidsms.backends.base import BackendBase

from rclickatell.models import Message


ERROR_SYNTAX = re.compile(r'ERR: (\d+), ([\w\s]+)')


class ClickatellBackend(BackendBase):
    '''A RapidSMS backend for Clickatell'''

    url = 'https://api.clickatell.com/http/sendmsg'

    def configure(self, user, password, api_id, callback=0):
        self.user = user
        self.password = password
        self.api_id = api_id
        self.callback = callback

    def run(self):    
        self.info('Clickatell configured (%s/%s)' % (self.user, self.api_id))
        super(ClickatellBackend, self).run()

    def _prepare_message(self, message):
        msg = Message.objects.create(body=message.text,
                                     connection=message.connection)
        data = {
            'user': self.user,
            'password': self.password,
            'api_id': self.api_id,
            'to': message.connection.identity,
            'text': message.text,
            'climsgid': msg.pk,
        }
        if self.callback > 0:
            data['deliv_ack'] = 1
            data['callback'] = self.callback
        return data

    def error_check(self, message):    
        matches = ERROR_SYNTAX.match(message)
        if matches:
            error_code = int(matches.group(1))
            error_message = matches.group(2)
            return error_code, error_message
        return None

    def send(self, message):
        data = self._prepare_message(message)
        self.debug('send: %s %s' % (message, data))
        response = urllib2.urlopen(self.url, urllib.urlencode(data))
        body = response.read()
        self.debug('Clicktell response: %s' % body)
        error = self.error_check(body)
        if error:
            error_code, error_message = error
            self.error('Clicktell error %d: %s' % (error_code, error_message))
