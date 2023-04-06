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

    # mohe
    'mohe.client',
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
    'mohe.datalab',

]

ROOT_URLCONF = 'mohe_api.urls'

WSGI_APPLICATION = 'mohe_api.wsgi.application'

AUTH_USER_MODEL = 'patient.Patient'

CSRF_TRUSTED_ORIGINS = [
    'http://admin.mohe.dev'
]
