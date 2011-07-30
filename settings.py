# Django settings for grepo project.

import sys
import os

import djcelery

rel = lambda *chunks: os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                  *chunks)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "apps"))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ("Your Name", "your_email@example.com"),
)

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": rel("dev.db"),
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

TIME_ZONE = None
LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_I18N = True
USE_L10N = True

STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")
STATIC_URL = "/static/"
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
#    "django.contrib.staticfiles.finders.DefaultStorageFinder",
)

SECRET_KEY = "ri$@i)-u(u%sc_k58zr$m#xf9xincz&r4qj2a%-$4#a1reg*$^"

TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
#     "django.template.loaders.eggs.Loader",
)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)

ROOT_URLCONF = "urls"

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "grepo_base.context_processors.grepo",
)

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",

    "south",
    "djcelery",

    "grepo_base",
    "grepo_opster",
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler"
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    }
}

# django-celery configuration
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

BROKER_USER = ""
BROKER_PASSWORD = ""
BROKER_BACKEND = "redis"
BROCKER_HOST = "localhost"
BROKER_PORT = 6379

REDIS_CONNECT_RETRY = True
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

CELERY_SEND_EVENTS = True
CELERY_RESULT_BACKEND = 'redis'
CELERY_TASK_RESULT_EXPIRES = 20

djcelery.setup_loader()

# -- grepo_base
GREPO_LANGUAGES = [
    "io",
    "erlang"
]
GREPO_BACKENDS = []


# -- grepo_opster
GREPO_NAME = "grepo"
GREPO_USAGE = "%name -L LANGUAGE [-n] RESULTS [KEYWORDS]"
GREPO_OPTIONS = [
    ("L", "language", "brainfuck",
      "programming language you want to grepo for"),
    ("n", "results", 20, "maximum number of projects to look up"),
]
