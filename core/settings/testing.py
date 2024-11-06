from .base import *
from os import path, environ
from dotenv.main import load_dotenv

DJANGO_ENV = 'testing'

SECRET_KEY = 'django-insecure-n*h7x8fzll&o8xzpal5h^t-(eyz+1=4pqf6ba329@$t4uu7ell'

DEBUG = True

env_file = '.env.test'
dotenv_path = path.join(BASE_DIR, env_file)
load_dotenv(dotenv_path=dotenv_path)




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get('DB_NAME'),
        'USER': environ.get('DB_USER'),
        'PASSWORD': environ.get('DB_PASS'),
        'HOST': environ.get('DB_HOST'),
        'PORT': environ.get('DB_PORT'),
    }
}
