"""
Django settings for cmv_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+z0e@uw7pm#5z)re78i^$j%8h)0r3nx13v@2x676@_@8i3)fo$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cmv_app',
    'south',
    'crispy_forms',
    'bootstrap3',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cmv_project.urls'

WSGI_APPLICATION = 'cmv_project.wsgi.application'

CRISPY_TEMPLATE_PACK = 'bootstrap3'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'cmv',
        'USER': 'cmv_user',
        'PASSWORD': 'cmv_pass',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

from django.core.urlresolvers import reverse_lazy

LOGIN_URL=reverse_lazy("login")
LOGIN_REDIRECT_URL=reverse_lazy("home")
LOGOUT_URL=reverse_lazy("logout")

TEMPLATE_LOADERS = (
   'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS=(os.path.join(BASE_DIR, 'templates'),)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
