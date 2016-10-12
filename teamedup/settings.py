"""
Django settings for gettingstarted project, on Heroku. For more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
import urlparse
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: change this before deploying to production!
SECRET_KEY = 'i+acxn5(akgsn!sr4^qgf(^m&*@+g1@u^t@=8s@axc41ml*f=s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'homepage',
    'app',
    'recruit',
    'teams',
    'api',
    'waffle',
    # leave at bottom otherwise some functionality like logout redirect breaks
    'django.contrib.admin',
    'django.contrib.sites',
    'django_comments',
    'storages',
    'sorl.thumbnail',
    'debug_toolbar',
)

THUMBNAIL_DEBUG = True
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'

INTERNAL_IPS = ('127.0.0.1',)

# SITE_ID for django.contrib.comments
SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'waffle.middleware.WaffleMiddleware',
)

ROOT_URLCONF = 'teamedup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'teamedup.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

ENV_PATH = os.path.abspath(os.path.dirname(__file__))

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

LOGIN_URL = '/app/login/'
LOGIN_REDIRECT_URL = '/app/login/'

# This is used by the `static` template tag from `static`, if you're using that. Or if anything else
# refers directly to STATIC_URL. So it's safest to always set it.


EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '') #TODO: move to env variables
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '') #TODO: it's not a good idea to store auth credentials like this
EMAIL_PORT = 587
EMAIL_USE_TLS = True

ACCOUNT_ACTIVATION_EMAIL = """
Hello %s,

Thank you for joining TeamedUp.
Activate your account by clicking this link: %s

Your friends at TeamedUp
"""

ORGANIZATION_INVITATION_EMAIL = """
Hello,

You were invited to join %s on TeamedUp.
Join it by clicking this link: %s

Your friends at TeamedUp
"""


try:
    os.environ['ENVIRONMENT'] == 'local'
    # DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    # use local media serving settings
    # MEDIA_ROOT = '/Users/nbyrne/Projects/teamedup/'
    MEDIA_ROOT = os.path.relpath('../')
    MEDIA_URL = '/media/'
except:
    # we'll use production settings
    # Static and media file caching setting
    AWS_HEADERS = {
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'Cache-Control': 'max-age=94608000',
    }
    # AWS S3 BUCKET DETAILS
    AWS_STORAGE_BUCKET_NAME = 'teamedup'
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    # Tell django-storages that when coming up with the URL for an item in S3 storage, keep
    # it simple - just use this domain plus the path. (If this isn't set, things get complicated).
    # This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
    # We also use it in the next setting.
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    ENV_PATH = os.path.abspath(os.path.dirname(__file__))
    MEDIA_ROOT = os.path.join(ENV_PATH, '/var/media/')  # '/var/media/'
    MEDIA_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN

    # Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
    # you run `collectstatic`).
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    redis_url = urlparse.urlparse(os.environ.get('REDIS_URL'))
    CACHES = {
        "default": {
            "BACKEND": "redis_cache.RedisCache",
            "LOCATION": "{0}:{1}".format(redis_url.hostname, redis_url.port),
            "OPTIONS": {
                "PASSWORD": redis_url.password,
                "DB": 0,
            }
        }
    }

# LOCAL SETTINGS THAT WE NEED TO CONFIGURE ENVIRONMENT LOGIC TO HANDLE CORRECTLY

try:
    from settings_local import *
except ImportError:
    pass
