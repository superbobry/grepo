# -*- coding: utf-8 -*-
"""
    grepo_base.github
    ~~~~~~~~~~~~~~~~~

"""
from datetime import datetime

from json import loads
from itertools import count
from httplib import HTTPConnection

from django.conf import settings

from grepo_base.models import Repository

#: Github api search path
SEARCH_PATH = "/api/v2/json/repos/search/language:{lang}?start_page={page}"
#: Github host, used for httplib for connect to api
GITHUB = "github.com"
#: List of languages that we will be processed
LANGUAGES = [lang[0].upper() + lang[1:] for lang in settings.GREPO_LANGUAGES]


def get_page(lang, page):
    connection = HTTPConnection(GITHUB)
    connection.request("GET", SEARCH_PATH.format(lang=lang, page=page))
    response = connection.getresponse()
    return response


def fetch_by_lang(lang):
    for page in count(1):
        page = get_page(lang, page)
        repositories = loads(page.read())["repositories"]
        if not repositories:
            break
        for repository in repositories:
            yield repository


def fetch_repositories():
    for lang in LANGUAGES:
        for repository in fetch_by_lang(lang):
            yield repository


def save_repository(repository):
    obj = Repository(url=repository["url"], name=repository["name"],
                     source=0,
                     language=LANGUAGES.index(repository["language"]),
                     summary=repository.get("description"),
                     updated_at=datetime.utcnow(), created_at=datetime.utcnow())
    obj.save()


def rescan_github():
    for repository in fetch_repositories():
        save_repository(repository)
