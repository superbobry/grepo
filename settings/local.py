# -*- coding: utf-8 -*-

from unipath import FSPath as Path

PROJECT_ROOT = Path(__file__).absolute().ancestor(2)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": PROJECT_ROOT.child("dev.db"),
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}


# -- django-celery

REDIS_CONNECT_RETRY = True
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

BROKER_HOST = REDIS_HOST
BROKER_PORT = REDIS_PORT
BROKER_VHOST = REDIS_DB
