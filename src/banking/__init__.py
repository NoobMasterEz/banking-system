THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'django_celery_beat',
    'django_celery_results',
    'drf_yasg',
]

API_APPS = [
    'banking.module.users',
    'banking.module.accounts',
]

LOCAL_APPS = [
    'banking.module.cores',

]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MAIN_APPS = list(
    DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS + API_APPS)
