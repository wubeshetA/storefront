import os
import dj_database_url
import sys
from .common import *


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = os.environ.get('DEBUG', False)

ALLOWED_HOSTS = ['storefront-nsnsl.ondigitalocean.app']

# db config in heroku
# DATABASES = {
#     'default': dj_database_url.config()  # this function look for env variable
#     # called DATABASE_URL and parse it to connection string
# }

if len(sys.argv) > 1 and sys.argv[1] != 'collectstatic':
    if os.getenv('DATABASE_URL', None) is None:
        raise Exception('DATABASE_URL environment variable not set')

    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL')),

    }
