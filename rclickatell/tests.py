import unittest
import urllib
import logging

from nose.tools import assert_equals, assert_raises, assert_true, assert_not_equals

from rapidsms.tests.harness import MockRouter
from rapidsms.models import Connection, Contact, Backend
from rapidsms.messages.outgoing import OutgoingMessage

from rclickatell.backend import ClickatellBackend
from rclickatell.models import Message, MessageStatus
from rclickatell.forms import StatusCallbackForm

from django.test import Client
from django.core.urlresolvers import reverse

logging.basicConfig(level=logging.DEBUG)
router = MockRouter()
backend = Backend.objects.create(name='Clickatell')
contact = Contact.objects.create(name='Test Contact')
connection = Connection.objects.create(contact=contact, backend=backend)


def test_outgoing_message():
    conf = {'user': 'test', 'password': 'abc', 'api_id': '1234'}
    clickatell = ClickatellBackend(name="clickatell", router=router, **conf)
    message = OutgoingMessage(connection, 'abc')
    data = clickatell._prepare_message(message)
    keys = ('user', 'password', 'api_id', 'to', 'text')
    for key in keys:
        assert_true(key in data)
    assert_equals('abc', data['text'])


def test_good_error_match():
    conf = {'user': 'test', 'password': 'abc', 'api_id': '1234'}
    clickatell = ClickatellBackend(name="clickatell", router=router, **conf)
    error = clickatell.error_check('ERR: 114, Cannot route message')
    assert_not_equals(error, None)
    code, message = error
    assert_equals(code, 114)
    assert_equals(message, 'Cannot route message')


def test_bad_error_match():
    conf = {'user': 'test', 'password': 'abc', 'api_id': '1234'}
    clickatell = ClickatellBackend(name="clickatell", router=router, **conf)
    error = clickatell.error_check('dfshkjadfshjlkadsfhlksadfhkj')
    assert_equals(error, None)


def test_status():
    client = Client()
    message = Message.objects.create(body='foo', connection=connection)

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
    assert_true(form.is_valid(), [(k, unicode(v[0])) for k, v in form.errors.items()])
    status = form.save(ip_address='127.0.0.1')
    assert_true(status.message_id, message.id)


def test_missing_from():
    message = Message.objects.create(body='foo', connection=connection)
    data = {
        'api_id': 12345,
        'apiMsgId': '996f364775e24b8432f45d77da8eca47',
        'cliMsgId': message.id,
        'timestamp': 1218007814,
        'to': 279995631564,
        'status': '003',
        'charge': '0.300000',
    }
    form = StatusCallbackForm(data)
    assert_true(form.is_valid(), [(k, unicode(v[0])) for k, v in form.errors.items()])
