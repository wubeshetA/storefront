import os
import dj_database_url
from .common import *


SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False

ALLOWED_HOSTS = ['wube-storefront.herokuapp.com']

DATABASES = {
    'default': dj_database_url.config() # this function look for env variable 
    # called DATABASE_URL and parse it to connection string
}