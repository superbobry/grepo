# -*- coding: utf-8 -*-

import sys

from unipath import FSPath as Path

PROJECT_ROOT = Path(__file__).absolute().ancestor(2)
sys.path.insert(0, PROJECT_ROOT.child("apps"))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ("Your Name", "your_email@example.com"),
)

MANAGERS = ADMINS

TIME_ZONE = None
LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_I18N = True
USE_L10N = True

STATIC_ROOT = PROJECT_ROOT.child("static")
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
    PROJECT_ROOT.child("templates"),
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


# -- django-celery

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

BROKER_BACKEND = "redis"

CELERY_SEND_EVENTS = True
CELERY_RESULT_BACKEND = "redis"
CELERY_TASK_RESULT_EXPIRES = 20


# -- grepo_base

GREPO_BACKENDS = [
    "grepo_base.backends.github.GithubBackend",
    "grepo_base.backends.lp.LaunchpadBackend",
]

LP_DIR = None

# -- grepo_opster

GREPO_NAME = "grepo"
GREPO_USAGE = "%name -l LANGUAGE [-o] RESULTS [KEYWORDS]"
GREPO_OPTIONS = [
    ("l", "language", "",
      "programming language you want to grepo for"),
    ("o", "only", 20, "maximum number of projects to look up"),
]
