import unittest
import urllib
import logging

from nose.tools import assert_equals, assert_raises, assert_true, assert_not_equals

from rapidsms.tests.harness import MockRouter
from rapidsms.models import Connection, Contact, Backend
from rapidsms.messages.outgoing import OutgoingMessage

from rclickatell.backend import ClickatellBackend


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
