# -*- coding: utf-8 -*-

from unipath import FSPath as Path

PROJECT_ROOT = Path(__file__).absolute().ancestor(2)

# -- django-celery

REDIS_CONNECT_RETRY = True
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
