import sys
import os
import imp

import pytest

import testproject.settings as config

def test_databases():
    os.environ['DATABASE_URL'] = 'postgres://fake:fake@fake.com/fake'
    imp.reload(config)
    
    assert 'postgres' in config.DATABASES['default']['ENGINE']

def test_test_runner():
    # Mock CI environment.
    os.environ['CI'] = '1'
    imp.reload(config)
    
    assert 'heroku' in config.TEST_RUNNER.lower()
    
    # Cleanup environment for further tests. 
    del os.environ['CI']
    
def test_staticfiles():
    imp.reload(config)
    
    assert config.STATIC_URL == '/static/'
    assert 'whitenoise' in config.MIDDLEWARE[0].lower()
    

def test_allowed_hosts():
    imp.reload(config)
    
    assert config.ALLOWED_HOSTS == ['*']
    
    
def test_logging():
    imp.reload(config)
    
    assert 'console' in config.LOGGING['handlers']
    
    
def test_secret_key():
    os.environ['SECRET_KEY'] = 'SECRET'

    imp.reload(config)
    assert config.SECRET_KEY == 'SECRET'
