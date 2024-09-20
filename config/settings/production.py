from config.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': os.environ.get('DB_NAME'),
    #     'USER': os.environ.get('DB_USER'),
    #     'PASSWORD': os.environ.get('DB_PASSWORD'),
    #     'HOST': os.environ.get('DB_HOST'),
    #     'PORT': os.environ.get('DB_PORT'),
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
