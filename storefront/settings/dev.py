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