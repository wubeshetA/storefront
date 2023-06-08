import os
import dj_database_url
from .common import *


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = False

ALLOWED_HOSTS = ['*']

# db config in heroku
# DATABASES = {
#     'default': dj_database_url.config()  # this function look for env variable
#     # called DATABASE_URL and parse it to connection string
# }
# DATABASES = {
#     'default': dj_database_url.config()  # this function look for env variable
#     # called DATABASE_URL and parse it to connection string
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'storefront',
        'HOST': 'storefront-postgres-server.postgres.database.azure.com',
        # 'PORT': '3306',
        'USER': 'wubeshet',
        'PASSWORD': os.getenv('AZURE_DB_PASSWORD'),
        'OPTIONS': {'sslmode': 'require'}
    },

}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# REDISCLOUD_URL = os.environ.get('REDISCLOUD_URL')
# CELERY_BROKER_URL = REDISCLOUD_URL

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "TIMEOUT": 60 * 10,  # 10 minutes
#         "LOCATION": REDISCLOUD_URL,
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# # }

# # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ.get('MAILGUN_SMTP_SERVER')
# EMAIL_HOST_USER = os.environ.get('MAILGUN_SMTP_LOGIN')
# EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD')
# EMAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT')
# # DEFAULT_FROM_EMAIL = 'admin@localhost'
