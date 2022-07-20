import os

import dj_database_url
from django.test.runner import DiscoverRunner

MAX_CONN_AGE = 600


class HerokuDiscoverRunner(DiscoverRunner):
    """Test Runner for Heroku CI, which provides a database for you.
    This requires you to set the TEST database (done for you by settings().)"""

    def setup_databases(self, **kwargs):
        if not os.environ.get('CI'):
            raise ValueError(
                "The CI env variable must be set to enable this functionality.  WARNING:  "
                "This test runner will wipe all tables in the 'public' schema "
                "of the database it targets!"
            )
        self.keepdb = True
        return super(HerokuDiscoverRunner, self).setup_databases(**kwargs)

    def _wipe_tables(self, connection):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    DROP SCHEMA public CASCADE;
                    CREATE SCHEMA public;
                    GRANT ALL ON SCHEMA public TO postgres;
                    GRANT ALL ON SCHEMA public TO public;
                    COMMENT ON SCHEMA public IS 'standard public schema'; 
                """
            )
        pass

    def teardown_databases(self, old_config, **kwargs):
        self.keepdb = True
        for connection, old_name, destroy in old_config:
            if destroy:
                self._wipe_tables(connection)
        super(HerokuDiscoverRunner, self).teardown_databases(
            old_config, **kwargs)


def settings(config, *, databases=True, test_runner=True, staticfiles=True, allowed_hosts=True, logging=True, secret_key=True):
    # Database configuration.
    if databases:
        # Integrity check.
        config['DATABASES'] = {'default': None}
        if 'DATABASE_URL' in os.environ:
            # Configure Django for DATABASE_URL environment variable.
            config['DATABASES']['default'] = dj_database_url.config(
                conn_max_age=config.get('CONN_MAX_AGE', MAX_CONN_AGE), ssl_require=True)

            # Enable test database if found in CI environment.
            if 'CI' in os.environ:
                config['DATABASES']['default']['TEST'] = config['DATABASES']['default']

    if test_runner:
        # Enable test runner if found in CI environment.
        if 'CI' in os.environ:
            config['TEST_RUNNER'] = 'django_heroku.HerokuDiscoverRunner'

    # Staticfiles configuration.
    if staticfiles:
        config['STATIC_ROOT'] = os.path.join(config['BASE_DIR'], 'staticfiles')
        config['STATIC_URL'] = '/static/'

        # Ensure STATIC_ROOT exists.
        os.makedirs(config['STATIC_ROOT'], exist_ok=True)

        # Insert Whitenoise Middleware.
        try:
            config['MIDDLEWARE_CLASSES'] = tuple(
                ['whitenoise.middleware.WhiteNoiseMiddleware'] + list(config['MIDDLEWARE_CLASSES']))
        except KeyError:
            config['MIDDLEWARE'] = tuple(
                ['whitenoise.middleware.WhiteNoiseMiddleware'] + list(config['MIDDLEWARE']))

        # Enable GZip.
        config['STATICFILES_STORAGE'] = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    # Generally avoid wildcards(*). However since Heroku router provides hostname validation it is ok
    if 'DYNO' in os.environ:
        config['ALLOWED_HOSTS'] = ['*']

    config['LOGGING'] = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                           'pathname=%(pathname)s lineno=%(lineno)s ' +
                           'funcname=%(funcName)s %(message)s'),
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            }
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'testlogger': {
                'handlers': ['console'],
                'level': 'INFO',
            }
        }
    }

    # SECRET_KEY configuration.
    if secret_key:
        if 'SECRET_KEY' in os.environ:
            # Set the Django setting from the environment variable.
            config['SECRET_KEY'] = os.environ['SECRET_KEY']
