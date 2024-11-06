from core.settings.base import *
from pathlib import Path
import os
from dotenv import load_dotenv


DJANGO_ENV = 'development'


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-n*h7x8fzll&o8xzpal5h^t-(eyz+1=4pqf6ba329@$t4uu7ell'
PERMIT_TOKEN = "permit_key_dyl2zhOIm2EXssDKP33JGbqGKKPiZarQjl0AcL7ZYvsYsLz2zFGDWcdRghccmR0EEJF5TS8c99g5ItDHl87alV"
PDP_SERVER = "http://localhost:7766"
DEBUG = True

KAFKA = {
'KAFKA_BROKER' : "localhost:9092",
'EVALUATION_TOPIC' : "evaluation",
'NOTIFICATION_TOPIC' : "student",
'EVALUATION_CONSUMER' : "evaluation-group",
'NOTIFICATION_CONSUMER' : "notification-group"
}
load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "staff",
        'USER': "staff",
        'PASSWORD': "staff",
        'HOST': "staff_db",
        'PORT': 5432,
        'TEST':{
            'NAME': "staff",
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
        }
    }
}

## if you don't have postgresql installed you can use sqlite3 (actualy you don't bcz sqlite doesnt have arrays in it's ds)

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }