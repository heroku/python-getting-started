
Django-Heroku (Python Library)
==============================

.. image:: https://travis-ci.org/heroku/django-heroku.svg?branch=master
    :target: https://travis-ci.org/heroku/django-heroku

This is a Django library for Heroku applications that ensures a seamless deployment and development experience.

This library provides:

-  Settings configuration (Static files / WhiteNoise).
-  Logging configuration.
-  Test runner (important for `Heroku CI <https://www.heroku.com/continuous-integration>`_).

--------------

Django 2.0 is targeted, but older versions of Django should be compatible. Only Python 3 is supported.

Usage of Django-Heroku
----------------------

In ``settings.py``, at the very bottom::

    …
    # Configure Django App for Heroku.
    import django_heroku
    django_heroku.settings(locals())

This will automatically configure ``DATABASE_URL``, ``ALLOWED_HOSTS``, WhiteNoise (for static assets), Logging, and Heroku CI for your application.

**Bonus points!** If you set the ``SECRET_KEY`` environment variable, it will automatically be used in your Django settings, too!

Disabling Functionality
///////////////////////

``settings()`` also accepts keyword arguments that can be passed ``False`` as a value, which will disable automatic configuration for their specific areas of responsibility:

- ``databases``
- ``test_runner``
- ``staticfiles``
- ``allowed_hosts``
- ``logging``
- ``secret_key``

-----------------------

You can also just use this library to provide a test runner for your Django application, for use on Heroku CI::

    import django_heroku
    TEST_RUNNER = 'django_heroku.HerokuDiscoverRunner'

✨🍰✨


