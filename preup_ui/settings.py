"""
Django settings for preup_ui project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from django import VERSION

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# Make it unique, and don't share it with anybody.
try:
    SECRET_KEY = open(os.path.join(DATA_DIR, 'secret_key')).read()
except:
    from django.utils.crypto import get_random_string
    SECRET_KEY = get_random_string(50, 'abcdefghijklmnopqrstuvwxyz0123456789@#$%^&*(-_=+)')
    open(os.path.join(DATA_DIR, 'secret_key'), 'w').write(SECRET_KEY)


DEBUG   = os.environ.get('DEBUG', False) and True or False
DBDEBUG = os.environ.get('DEBUG', False) == 'DB'
TEMPLATE_DEBUG = os.environ.get('DEBUG', False) == 'TEMPLATE'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'preup_ui.report',
    'preup_ui.config',
    'preup_ui.xmlrpc_backend',
    'preup_ui',
)

if VERSION < (1, 7):
    INSTALLED_APPS += ('south',)
    SOUTH_MIGRATION_MODULES = {
        'preup_ui.report': 'preup_ui.report.south_migrations',
        'preup_ui.config': 'preup_ui.config.south_migrations',
    }

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
if VERSION >= (1, 7):
    MIDDLEWARE_CLASSES += (
        'django.contrib.messages.middleware.MessageMiddleware',
    )
MIDDLEWARE_CLASSES += (
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'preup_ui.exception_middleware.ExceptionMiddleware',
)

ROOT_URLCONF = 'preup_ui.urls'

WSGI_APPLICATION = 'preup_ui.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATA_DIR, 'db.sqlite'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

# oscap doesn't provide TZ aware dates anyway
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(DATA_DIR, 'static')

MEDIA_URL = '/upload/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'upload')

RESULTS_DIR = os.path.join(DATA_DIR, 'results')


from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'preup_ui.auth.context_processors.auth_enabled',
)


AUTHENTICATION_BACKENDS = (
    'preup_ui.auth.backends.AutologinBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = 'auth-login'
LOGIN_REDIRECT_URL = '/'
LOGIN_EXEMPT_URLS = ['^xmlrpc/', '^submit/', '^login/', '^admin/', '^first/']

if DEBUG:
    opt_apps = ['django_extensions', 'debug_toolbar']
    for mod in opt_apps:
        try:
            __import__(mod)
        except ImportError:
            pass
        else:
            INSTALLED_APPS += (mod,)


XMLRPC_METHODS = {
    'submission': (
        ('preup_ui.xmlrpc.submission', 'submit'),
    ),
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': DEBUG and 'DEBUG' or 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'level': DBDEBUG and 'DEBUG' or 'INFO',
            'propagate': True,
        },
    },
}

