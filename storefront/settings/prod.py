import os
import dj_database_url
from .common import *


SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False

ALLOWED_HOSTS = ['wube-storefront.herokuapp.com']

DATABASES = {
    'default': dj_database_url.config()  # this function look for env variable
    # called DATABASE_URL and parse it to connection string
}

REDISCLOUD_URL = os.environ.get('REDISCLOUD_URL')
CELERY_BROKER_URL = REDISCLOUD_URL

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "TIMEOUT": 60 * 10,  # 10 minutes
        "LOCATION": REDISCLOUD_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('MAILGUN_SMTP_SERVER')
EMAIL_HOST_USER = os.environ.get('MAILGUN_SMTP_LOGIN')
EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD')
EMAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT')
# DEFAULT_FROM_EMAIL = 'admin@localhost'
