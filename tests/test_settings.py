# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "77777777777777777777777777777777777777777777777777"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'postgres',  # Or path to database file if using sqlite3.
        'USER': 'postgres',  # Not used with sqlite3.
        'PASSWORD': 'postgres',  # Not used with sqlite3.
        'HOST': 'localhost',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',  # Set to empty string for default. Not used with sqlite3.
    }
}

# ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "user",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "ajax_datatable",
]

AUTH_USER_MODEL = "user.TestUser"

SITE_ID = 1

MIDDLEWARE = ()


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]
