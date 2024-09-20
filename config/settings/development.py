from config.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('NAME'),
        'USER': os.environ.get('USER'),
        "PASSWORD": os.environ.get('PASSWORD'),
        "HOST": os.environ.get('HOST'),
        "PORT": os.environ.get('PORT'),
    }
}
