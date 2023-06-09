from .common import *


SECRET_KEY = 'django-insecure-n2ik^e1^@yjbyq%$0u7d*wy-gr%5-$*^!f(5x&s1$!#acikjer'
DEBUG = True

# db config for my mysql
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'storefront',
#         'HOST': 'localhost',
#         # 'PORT': '3306',
#         'USER': 'root',
#         'PASSWORD': os.getenv("DB_PASSWORD"),
#     }
# }

# db config for postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'storefront',
        'HOST': 'localhost',
        # 'PORT': '3306',
        'USER': 'postgres',
        'PASSWORD': os.getenv("DB_PASSWORD"),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'storefront',
#         'HOST': 'storefront-postgres-server.postgres.database.azure.com',
#         # 'PORT': '3306',
#         'USER': 'wubeshet',
#         'PASSWORD': os.getenv('AZURE_DB_PASSWORD'),
#         'OPTIONS': {'sslmode': 'require'}
#     },

# }

# CELERY_BROKER_URL = 'redis://localhost:6379/1'

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "TIMEOUT": 60 * 10,  # 10 minutes
#         "LOCATION": "redis://127.0.0.1:6379/2",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'localhost'
# EMAIL_HOST_USER = ''
# # EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 2525
# DEFAULT_FROM_EMAIL = 'admin@localhost'
