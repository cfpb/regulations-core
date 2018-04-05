"""Base settings file; used by manage.py. All settings can be overridden via
local_settings.py"""
import os

from django.utils.crypto import get_random_string

import dj_database_url


INSTALLED_APPS = [
    'haystack',
    'regcore',
    'regcore_read',
    'regcore_write',
]
MIDDLEWARE_CLASSES = []

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', get_random_string(50))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'eregs.db'
    }
}

if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config()

TEST_RUNNER = 'django_nose.runner.NoseTestSuiteRunner'

ROOT_URLCONF = 'regcore.urls'

DEBUG = True

BACKENDS = {
    'regulations': 'regcore.db.django_models.DMRegulations',
    'layers': 'regcore.db.django_models.DMLayers',
    'notices': 'regcore.db.django_models.DMNotices',
    'diffs': 'regcore.db.django_models.DMDiffs'
}

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=regcore,regcore_read,regcore_write'
]

ELASTIC_SEARCH_URLS = []
ELASTIC_SEARCH_INDEX = 'eregs'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    }
}

try:
    from local_settings import *
except ImportError:
    pass
