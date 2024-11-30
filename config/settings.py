import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-o*76t9ob(w+(f@$_-kc!6eh248m$*de71i3wr%tccfe2s3jpc)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    "account",
    "core",
    "card",
    "order"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "account.middleware.AjaxMiddleware"
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
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

WSGI_APPLICATION = 'config.wsgi.application'




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



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




LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATICFILES_DIRS=[BASE_DIR,"static"]

MEDIA_URL="/media/"
MEDIA_ROOT=os.path.join(BASE_DIR,"media")



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL="account.User"



THROTTLE_ZONES = {
    'default': {
        'VARY':'throttle.zones.RemoteIP',
        'NUM_BUCKETS':2,  # Number of buckets worth of history to keep. Must be at least 2
        'BUCKET_INTERVAL':40 * 60,  # Period of time to enforce limits.
        'BUCKET_CAPACITY':20,  # Maximum number of requests allowed within BUCKET_INTERVAL
    },

    'mymy': {
        'VARY':'throttle.zones.RemoteIP',
        'NUM_BUCKETS':2,  # Number of buckets worth of history to keep. Must be at least 2
        'BUCKET_INTERVAL':5 * 60,  # Period of time to enforce limits.
        'BUCKET_CAPACITY':1,  # Maximum number of requests allowed within BUCKET_INTERVAL
    },
    "resend":
    {
        'VARY':'throttle.zones.RemoteIP',
        'NUM_BUCKETS':2,  # Number of buckets worth of history to keep. Must be at least 2
        'BUCKET_INTERVAL':1 * 60,  # Period of time to enforce limits.
        'BUCKET_CAPACITY':4,  # Maximum number of requests allowed within BUCKET_INTERVAL
    },
}

THROTTLE_BACKEND = 'throttle.backends.cache.CacheBackend'
THROTTLE_ENABLED = True


# kavehnegar sms

KAVEHNEGAR_KEY='71456537783936513335477935536F64584334596C3639424C6143474C48767536696F7A364558395A34633D'
SENDER_NUMBER='09981000176'
KAVEHNEGAR_CUSTOM_TEMPLATE_MYSELF_VAR = 'Identification'



