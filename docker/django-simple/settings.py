"""
Django settings for zkcluster project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

def str2bool(cadena):
    """retorna un booleano a partir de una cadena [yes,true,t] o numero 1 """
    return cadena.lower() in ("yes", "true", "t", "1")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = (os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    with open(os.path.join(BASE_DIR, 'secretkey.txt')) as f:
        SECRET_KEY = f.read().strip()
except FileNotFoundError as e:
    SECRET_KEY = "please generate the secret.txt file first! python manage.py generate_secret_key"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str2bool(os.getenv('DEBUG', "False"))

#must set if debug is false
ALLOWED_HOSTS = ['*'] # TODO: must populate with docker host

#ZKcluster options!
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

ZK_CLUSTER = {
    'TERMINAL_TIMEOUT': 5, # default timeout
    'OMMIT_PING': False, # for systems without ping
    'VERBOSE': DEBUG # for debuging communication
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_generate_secret_key',
    'zkcluster'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if os.path.isfile(os.path.join(BASE_DIR, 'Pipfile')):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('PGDATABASE', 'zkcluster'),
            'USER': os.getenv('PGUSER', 'zkcluster'),
            'PASSWORD': os.getenv('PGPASSWORD', '********'),
            'HOST': os.getenv('PGHOST', 'zkcluster-db'),
            'PORT': int(os.getenv('PGPORT', '5432')),
        }
    }
else: # develop without docker
    print ("WRN: Using Sqlite!")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = os.getenv('LANGUAGE', 'en-us')

TIME_ZONE = os.getenv('TIMEZONE', 'America/La_Paz')

USE_I18N = True

#LOCALE_PATHS = [
#    os.path.join(BASE_DIR, 'zkcluster/locale'),
#]

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
