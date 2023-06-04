from .common import *


SECRET_KEY = 'django-insecure-n2ik^e1^@yjbyq%$0u7d*wy-gr%5-$*^!f(5x&s1$!#acikjer'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront',
        'HOST': 'localhost',
        # 'PORT': '3306',
        'USER': 'root',
        'PASSWORD': os.getenv("DB_PASSWORD"),
    }
}
CELERY_BROKER_URL = 'redis://localhost:6379/1'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "TIMEOUT": 60 * 10,  # 10 minutes
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
