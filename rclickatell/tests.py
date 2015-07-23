import unittest
import urllib
import logging

from rapidsms.tests.harness import MockRouter
from rapidsms.models import Connection, Contact, Backend
from rapidsms.messages.outgoing import OutgoingMessage

from rclickatell.backend import ClickatellBackend
from rclickatell.models import Message, MessageStatus
from rclickatell.forms import StatusCallbackForm

from django.test import Client, TestCase
from django.core.urlresolvers import reverse

logging.basicConfig(level=logging.DEBUG)


class ClickatellTest(TestCase):

    def setUp(self):
        self.router = MockRouter()
        self.backend = Backend.objects.create(name='Clickatell')
        self.contact = Contact.objects.create(name='Test Contact')
        self.connection = Connection.objects.create(contact=self.contact, backend=self.backend)

    def test_outgoing_message(self):
        conf = {'user': 'test', 'password': 'abc', 'api_id': '1234'}
        clickatell = ClickatellBackend(name="clickatell", router=self.router, **conf)
        message = OutgoingMessage([self.connection], 'abc')
        msg, data = clickatell._prepare_message(message)
        keys = ('user', 'password', 'api_id', 'to', 'text')
        for key in keys:
            self.assertTrue(key in data)
        self.assertEqual('abc', data['text'])

    def test_good_error_match(self):
        conf = {'user': 'test', 'password': 'abc', 'api_id': '1234'}
        clickatell = ClickatellBackend(name="clickatell", router=self.router, **conf)
        error = clickatell.error_check('ERR: 114, Cannot route message')
        self.assertNotEqual(error, None)
        code, message = error
        self.assertEqual(code, 114)
        self.assertEqual(message, 'Cannot route message')

    def test_bad_error_match(self):
        conf = {'user': 'test', 'password': 'abc', 'api_id': '1234'}
        clickatell = ClickatellBackend(name="clickatell", router=self.router, **conf)
        error = clickatell.error_check('dfshkjadfshjlkadsfhlksadfhkj')
        self.assertEqual(error, None)

    def test_good_id_match(self):
        conf = {'user': 'test', 'password': 'abc', 'api_id': '1234'}
        clickatell = ClickatellBackend(name="clickatell", router=self.router, **conf)
        api_id = clickatell.id_check('ID: d9bb8bebc6258fe47a76988f81a96634')
        self.assertNotEqual(api_id, None)
        self.assertEqual(api_id, 'd9bb8bebc6258fe47a76988f81a96634')

    def test_bad_id_match(self):
        conf = {'user': 'test', 'password': 'abc', 'api_id': '1234'}
        clickatell = ClickatellBackend(name="clickatell", router=self.router, **conf)
        api_id = clickatell.id_check('dfshkjadfshjlkadsfhlksadfhkj')
        self.assertEqual(api_id, None)

    def test_status(self):
        client = Client()
        message = Message.objects.create(body='foo', connection=self.connection)

        data = {
            'api_id': 12345,
            'apiMsgId': '996f364775e24b8432f45d77da8eca47',
            'cliMsgId': message.id,
            'timestamp': 1218007814,
            'to': 279995631564,
            'from': 27833001171,
            'status': '003',
            'charge': '0.300000',
        }
        form = StatusCallbackForm(data)
        self.assertTrue(form.is_valid(), [(k, unicode(v[0])) for k, v in form.errors.items()])
        status = form.save(ip_address='127.0.0.1')
        self.assertTrue(status.message_id, message.id)

    def test_missing_from(self):
        message = Message.objects.create(body='foo', connection=self.connection)
        data = {
            'api_id': 12345,
            'apiMsgId': '996f364775e24b8432f45d77da8eca47',
            'cliMsgId': message.id,
            'timestamp': 1218007814,
            'to': 279995631564,
            'from': '',
            'status': '003',
            'charge': '0.300000',
        }
        form = StatusCallbackForm(data)
        self.assertTrue(form.is_valid(), [(k, unicode(v[0])) for k, v in form.errors.items()])
        status = form.save(ip_address='127.0.0.1')
        self.assertEqual(status.sender, '')
