import logging
import os

import dj_database_url
from django.test.runner import DiscoverRunner

MAX_CONN_AGE = 600

logger = logging.getLogger(__name__)


class HerokuDiscoverRunner(DiscoverRunner):
    """Test Runner for Heroku CI, which provides a database for you.
    This requires you to set the TEST database (done for you by settings().)"""

    def setup_databases(self, **kwargs):
        if not os.environ.get('CI'):
            raise ValueError(
                "The CI env variable must be set to enable this functionality.  WARNING:  "
                "This test runner will wipe all tables in the database it targets!")
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
        super(HerokuDiscoverRunner, self).teardown_databases(old_config, **kwargs)


def settings(config, *, db_colors=False, databases=True, test_runner=True, staticfiles=True, allowed_hosts=True, logging=True, secret_key=True):

    # Database configuration.
    # TODO: support other database (e.g. TEAL, AMBER, etc, automatically.)
    if databases:
        # Integrity check.
        if 'DATABASES' not in config:
            config['DATABASES'] = {'default': None}

        if db_colors:
            # Support all Heroku databases.
            # TODO: This appears to break TestRunner.
            for (env, url) in os.environ.items():
                if env.startswith('HEROKU_POSTGRESQL'):
                    db_color = env[len('HEROKU_POSTGRESQL_'):].split('_')[0]

                    logger.info('Adding ${} to DATABASES Django setting ({}).'.format(env, db_color))

                    config['DATABASES'][db_color] = dj_database_url.parse(url, conn_max_age=MAX_CONN_AGE, ssl_require=True)

        if 'DATABASE_URL' in os.environ:
            logger.info('Adding $DATABASE_URL to default DATABASE Django setting.')

            # Configure Django for DATABASE_URL environment variable.
            config['DATABASES']['default'] = dj_database_url.config(conn_max_age=MAX_CONN_AGE, ssl_require=True)

            logger.info('Adding $DATABASE_URL to TEST default DATABASE Django setting.')

            # Enable test database if found in CI environment.
            if 'CI' in os.environ:
                config['DATABASES']['default']['TEST'] = config['DATABASES']['default']

        else:
            logger.info('$DATABASE_URL not found, falling back to previous settings!')

    if test_runner:
        # Enable test runner if found in CI environment.
        if 'CI' in os.environ:
            config['TEST_RUNNER'] = 'django_heroku.HerokuDiscoverRunner'

    # Staticfiles configuration.
    if staticfiles:
        logger.info('Applying Heroku Staticfiles configuration to Django settings.')

        config['STATIC_ROOT'] = os.path.join(config['BASE_DIR'], 'staticfiles')
        config['STATIC_URL'] = '/static/'

        # Ensure STATIC_ROOT exists.
        os.makedirs(config['STATIC_ROOT'], exist_ok=True)

        # Insert Whitenoise Middleware.
        try:
            config['MIDDLEWARE_CLASSES'] = tuple(['whitenoise.middleware.WhiteNoiseMiddleware'] + list(config['MIDDLEWARE_CLASSES']))
        except KeyError:
            config['MIDDLEWARE'] = tuple(['whitenoise.middleware.WhiteNoiseMiddleware'] + list(config['MIDDLEWARE']))

        # Enable GZip.
        config['STATICFILES_STORAGE'] = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    if allowed_hosts:
        logger.info('Applying Heroku ALLOWED_HOSTS configuration to Django settings.')
        config['ALLOWED_HOSTS'] = ['*']

    if logging:
        logger.info('Applying Heroku logging configuration to Django settings.')

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
            logger.info('Adding $SECRET_KEY to SECRET_KEY Django setting.')
            # Set the Django setting from the environment variable.
            config['SECRET_KEY'] = os.environ['SECRET_KEY']

