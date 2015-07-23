#!/usr/bin/env python
import logging
import sys

import django
from django.conf import settings


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'rapidsms',
            'rclickatell',
        ),
        SECRET_KEY='super-secret',
        MIDDLEWARE_CLASSES=(
        ),
        INSTALLED_BACKENDS={
            'clickatell-backend': {
                'ENGINE': 'rclickatell.backend.ClickatellBackend',
                'user': '',
                'password': '',
                'api_id': '',
                'callback': 3,
            }
        },
    )


from django.test.utils import get_runner


def runtests():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    django.setup()

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=True, failfast=False)
    args = sys.argv[1:] or []
    failures = test_runner.run_tests(args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
