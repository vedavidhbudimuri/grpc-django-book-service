"""
Django settings for grpc_book_service_backend project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development conf - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/


ALLOWED_HOSTS = [
    "grpc-book-service-backend-alpha.apigateway.in",
    "127.0.0.1",
    "localhost"
]

ROOT_URLCONF = 'grpc_book_service_backend.urls'

CSRF_COOKIE_SECURE = False

WSGI_APPLICATION = 'grpc_book_service_backend.wsgi.application'

SCRIPT_NAME = "/" + os.environ.get("STAGE", "alpha")

################## CORS #####################

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    '127.0.0.1',
)

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'x-api-key',
    'x-source'
)
# *************** Internationalization *******************#
# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False

RAVEN_CONFIG = {
    'dsn': os.environ.get("RAVEN_DSN"),
    'release': os.environ.get('STAGE')
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        }
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            "filters": ["request_id"],
        }
    },
    'formatters': {
        'console': {
            'format': "[%(request_id)s] [grpc_book_service_backend - " + os.environ.get(
                "STAGE", "local") +
                      '] %(levelname)-8s [%(asctime)s]  '
                      '[%(pathname)s] [%(filename)s]'
                      '[%(funcName)s] [%(lineno)d]: %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },
    'loggers': {
        'segment': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        '': {
            'handlers': ['console', 'sentry', ],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
# ********************** Installed Apps ****************************

INSTALLED_APPS = [
    'django.contrib.admin',  # admin interface
    'django.contrib.auth',  # django authentication
    'django.contrib.contenttypes',  # response content types used in admin
    'django.contrib.sessions',  # django sessions used in admin
    'django.contrib.messages',
    # info, success, error message in response. admin requires this
    'django.contrib.staticfiles',  # host the static files
]

THIRD_PARTY_APPS_BASE = [
    # oauth
    'oauth',
    'oauth2_provider',
    # aws storage
    'storages',
    # django rest framework
    'rest_framework',
    'rest_framework_xml',  # xml renderers, parsers
    'corsheaders',

    # raven
    'raven.contrib.django.raven_compat',
    # django fine uploader
    'django_fine_uploader_s3',

]
INSTALLED_APPS += THIRD_PARTY_APPS_BASE

# ********************** Password Validators ***************************
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

# ************************* Django Rest Framework ******************************
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
        'rest_framework_xml.parsers.XMLParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
        'rest_framework.renderers.AdminRenderer',
    )
}

# ************************** Templates ******************************
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# *********************** Middleware *************************#

MIDDLEWARE = [
    'log_request_id.middleware.RequestIDMiddleware',  # request logging
    'django.contrib.sessions.middleware.SessionMiddleware',
    # django sessions, usefull in admin
    'corsheaders.middleware.CorsMiddleware',  # cors headers middleware
    'django.middleware.common.CommonMiddleware',
    # handling the url redirect, adding / in the end of url.
    # ref https://docs.djangoproject.com/en/1.9/ref/middleware/#django.middleware.common.CommonMiddleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # set request.user value after authenticating
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # used in session invalidation, admin requires this
    'django.contrib.messages.middleware.MessageMiddleware',
    # messaging framework middleware, django admin requires this
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # save from clickjack attack ref https://docs.djangoproject.com/en/1.9/ref/clickjacking/
    'django.middleware.locale.LocaleMiddleware',
]

from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
    ('en', _('English')),
    ('te', _('Telugu')),
    ('hi', _('Hindi')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
