-*- restructuredtext -*-

rapidsms-clickatell
===================

rclickatell is a basic `Clickatell <http://www.twilio.com>`_ backend for the
`RapidSMS <http://www.rapidsms.org/>`_ project. Currently, rclickatell only
supports Mobile Terminated (MT) SMS communication (sending outgoing messages
using the Clickatell API), but could be extended in the future to support
Mobile Originated (MO) messages.

Requirements
------------

* `Django <http://www.djangoproject.com/>`_ >= 1.2
* `RapidSMS <http://www.rapidsms.org/>`_ >= 0.9.3a

Installation
------------

You can install rclickatell in a few ways:

 * Download rclickatell and run: ``python setup.py install``
 * Or, using pip: ``pip install -e git+http://github.com/caktus/rapidsms-clickatell.git#egg=rclickatell``

Features and Settings
---------------------

 * Status Notification: rclickatell can be configured to enable Clickatell's
   callback functionality. When setup, after sending a an outgoing message,
   Clickatell will ping the callback URL defined in your Clickatell API
   account.

Usage
-----

Once rclickatell is installed, add it to ``INSTALLED_APPS`` and ``INSTALLED_BACKENDS`` in settings.py::

    INSTALLED_APPS (
        ...
        'rclickatell',
        ...
    )

    INSTALLED_BACKENDS = {
        "clickatell": {
            "ENGINE": "rclickatell.backend"
            'user': '',
            'password': '',
            'api_id': '',
            'callback' 3, # enable (levels 1-3) to enable Clickatell status notifications
        },
    }
