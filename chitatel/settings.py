"""
=================
chitatel.settings
=================

Settings for chitatel project.

"""

import sys

import dj_database_url

from chitatel.utils import BOOL, ENV, dict_combine, import_settings, rel


# Debug settings
DEBUG = BOOL(ENV('DEBUG', True))
TEMPLATE_DEBUG = DEBUG

# Database settings
DATABASES = {
    'default': dj_database_url.config() or {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'chitatel',
        'USER': 'chitatel',
        'PASSWORD': 'chitatel',
        'HOST': '127.0.0.1',
        'PORT': 5432,
    }
}

# Date and time settings
TIME_ZONE = ENV('TIME_ZONE', 'Europe/Kiev')
USE_TZ = BOOL(ENV('USE_TZ', True))

# Installed applications
INSTALLED_APPS = (
    # Django applications
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    # 3rd party applications
    'debug_toolbar',
    'django_extensions',
    'south',

    # Our applications
    'chitatel',
    'feeds',
    'users',
)
LOCAL_INSTALLED_APPS = ()

# Locale settings
LANGUAGE_CODE = ENV('LANGUAGE_CODE', 'ru')
USE_I18N = BOOL(ENV('USE_I18N', True))
USE_L10N = BOOL(ENV('USE_L10N', True))

# Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(asctime)s [%(levelname)s:%(name)s] %(message)s',
        },
        'naked': {
            'format': u'%(message)s',
        }
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'INFO',
            'stream': sys.stdout,
        },
        'stderr': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'ERROR',
            'stream': sys.stderr,
        }
    },
    'loggers': {
        'celery': {
            'handlers': ['stderr', 'stdout'],
            'level': 'INFO',
        },
        'chitatel': {
            'handlers': ['stderr', 'stdout'],
            'level': 'INFO',
        },
        'feeds': {
            'handlers': ['stderr', 'stdout'],
            'level': 'INFO',
        },
        'users': {
            'handlers': ['stderr', 'stdout'],
            'level': 'INFO',
        },
    }
}
LOCAL_LOGGING = {}

# Middleware settings
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Sentry settings
SENTRY_DSN = ENV('SENTRY_DSN', 'Sentry DSN URL')

# Static files settings
STATIC_ROOT = rel('..', 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Other settings
ALLOWED_HOSTS = ['127.0.0.1']
ROOT_URLCONF = 'chitatel.urls'
SECRET_KEY = 'please, set proper secret key in local settings'
WSGI_APPLICATION = 'chitatel.wsgi.application'

# Load settings from our apps
import_settings('feeds.settings', locals())
import_settings('users.settings', locals())

# Load local settings, but only if they exists
import_settings('chitatel.settings_local', locals(), True)


# Update installed apps
INSTALLED_APPS = INSTALLED_APPS + LOCAL_INSTALLED_APPS

# Update logging settings to use Sentry
if SENTRY_DSN.startswith('https://'):
    LOGGING['handlers'].update({
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.handlers.logging.SentryHandler',
            'dsn': SENTRY_DSN,
        }
    })
    LOGGING['loggers']['celery']['handlers'].append('sentry')
    LOGGING['loggers']['chitatel']['handlers'].append('sentry')
    LOGGING['loggers']['feeds']['handlers'].append('sentry')
    LOGGING['loggers']['users']['handlers'].append('sentry')

# Add local loging settings
dict_combine(LOGGING, LOCAL_LOGGING, False)
