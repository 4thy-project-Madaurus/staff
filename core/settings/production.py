from core.settings.base import *
from dotenv import load_dotenv
from os import environ, path

DJANGO_ENV = 'production'

# env_file = '.env.prod'
# dotenv_path = path.join(BASE_DIR, env_file)


load_dotenv()


SECRET_KEY = environ.get("SECRET_KEY")

DEBUG = False


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


KAFKA = {
'KAFKA_BROKER' : environ.get('KAFKA_BROKER'),
'EVALUATION_TOPIC' : "evaluation",
'NOTIFICATION_TOPIC' : "student",
'EVALUATION_CONSUMER' : "evaluation-group",
'NOTIFICATION_CONSUMER' : "notification-group"
}

PERMIT_TOKEN = environ.get("PERMIT_TOKEN")
PDP_SERVER = environ.get("PDP_SERVER")
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


KAFKA = {
'KAFKA_BROKER' : environ.get('KAFKA_BROKER'),
'EVALUATION_TOPIC' : "evaluation",
'NOTIFICATION_TOPIC' : "student",
'EVALUATION_CONSUMER' : "evaluation-group",
'NOTIFICATION_CONSUMER' : "notification-group"
}


ALLOWED_HOSTS = ['*']




CORS_ALLOW_ALL_ORIGINS = True




