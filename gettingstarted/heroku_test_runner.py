import os

from django.test.runner import DiscoverRunner

"""
WARNING:  WHEN USED INCORRECTLY THIS TEST RUNNER WILL DROP ALL TABLES IN YOUR PRODUCTION 
DATABASE!!!

Heroku does not give users createdb/dropdb permissions, therefore Heroku CI cannot run tests for django.
In order to fix this, use this test runner instead which attempts to minimally override the 
default test runner by a)  forcing keepdb=True to stop database create/drop, and b) by dropping all
tables after a test run and resetting the database to its initial blank state.

Usage:

1. In your django test settings file add the following two lines to ensure that the test 
database name is the same as the Heroku provided database name.

DATABASES['default'] = env.db('DATABASE_URL')  # or whatever you use to load the Heroku database settings
DATABASES['default']['TEST'] = {'NAME': DATABASES['default']['NAME']}

2. Set the testrunner to this file
TEST_RUNNER = 'your_modules.HerokuDiscoverRunner'

3. Set an environment variable on heroku CI of IS_HEROKU_TEST=1 to enable this runner, otherwise
the runner will exit as a safety measure.
"""

class HerokuDiscoverRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        if not os.environ.get('IS_HEROKU_TEST'):
            raise ValueError(
                "The IS_HEROKU_TEST env variable must be set to enable this.  WARNING:  "
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

    def teardown_databases(self, old_config, **kwargs):
        self.keepdb = True
        for connection, old_name, destroy in old_config:
            if destroy:
                self._wipe_tables(connection)
        super(HerokuDiscoverRunner, self).teardown_databases(old_config, **kwargs)
