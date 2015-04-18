import os

from configurations import Configuration
from configurations import values


def path(*components):
    root = os.path.dirname(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(root, *components))


class ConstantSettings(Configuration):
    """
    These settings are unlikely to need changing in an environment.

    These are more like constants that make the app work. They may change as
    the app is developed, but they likely should not be overridden by the
    environment.
    """

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'jyfes.viewer',
    ]

    MIDDLEWARE_CLASSES = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
    ]

    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.jinja2.Jinja2',
            'APP_DIRS': True,
            'OPTIONS': {
                'environment': 'jyfes.lib.jinja2.environment',
            },
        },
    ]

    ROOT_URLCONF = 'jyfes.urls'
    USE_TZ = True
    USE_L10N = False

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                           'pathname=%(pathname)s lineno=%(lineno)s ' +
                           'funcname=%(funcName)s %(message)s'),
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True,
            }
        }
    }


class Base(ConstantSettings):
    """
    These settings will likely need to be customized to an environment.
    """
    ALLOWED_HOSTS = values.ListValue([])
    DEBUG = values.BooleanValue(False)
    SECRET_KEY = values.SecretValue()
    TIME_ZONE = values.Value('UTC')
    LANGUAGE_CODE = values.Value('en-us')
    STATIC_URL = values.Value('/static/')
    STATIC_ROOT = values.Value(path('static'))


class Dev(Base):
    DEBUG = True
    SECRET_KEY = 'not a secret'


class Test(Base):
    SECRET_KEY = 'not a secret'
