from mohe.settings.base import *

# Application definition

INSTALLED_APPS = [
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'rest_framework',
    'rest_framework.authtoken',

    # mohe
    'mohe.client',
    'mohe.demo',
    'mohe.diagnostics',
    'mohe.hardware',
    'mohe.kplex',
    'mohe.geo',
    'mohe.patient',
    'mohe.measurement',
    'mohe.supply',
    'mohe.util',
    'mohe.alert',
    'mohe.ui',

    'mohe_api.api_tests',
]

ROOT_URLCONF = 'mohe_api.urls'

WSGI_APPLICATION = 'mohe_api.wsgi.application'

AUTH_USER_MODEL = 'patient.Patient'

CSRF_TRUSTED_ORIGINS = [
    'http://admin.demo.mohe.ch'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}
