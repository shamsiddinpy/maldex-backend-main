from config.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'prod_db',
        'USER': 'modago',
        "PASSWORD": "dbpass",
        "HOST": "localhost",
        "PORT": 5432,
    }
}
