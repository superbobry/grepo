# -*- coding: utf-8 -*-

from bundle_config import config

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": config["postgres"]["database"],
#         "USER": config["postgres"]["username"],
#         "PASSWORD": config["postgres"]["password"],
#         "HOST": config["postgres"]["host"],
#     }
# }

CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "{0[host]}:{0[port]}".format(config["redis"]),
        "OPTIONS": {
            "PASSWORD": config["redis"]["password"],
        },
        "VERSION": config["core"]["version"],
    },
}


# -- django-celery

REDIS_CONNECT_RETRY = True
REDIS_HOST = config["redis"]["host"]
REDIS_PORT = config["redis"]["port"]
REDIS_DB = 0
