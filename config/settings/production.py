from config.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ['*']


DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'prod_db',
    #     'USER': 'modago',
    #     'PASSWORD': '1',
    #     'HOST': 'localhost',
    #     'PORT': '5432',
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'maldex',
        'USER': 'maldex_user',
        'PASSWORD': 'pass4ord',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
