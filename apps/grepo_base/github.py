# -*- coding: utf-8 -*-
"""
    grepo_base.github
    ~~~~~~~~~~~~~~~~~

"""

from json import loads
from itertools import count
from httplib import HTTPConnection

#: Github api search path
SEARCH_PATH = "/api/v2/json/repos/search/language:{lang}?start_page={page}"
#: Github host, used for httplib for connect to api
GITHUB = "github.com"
#: List of languages that we will be processed
LANGUAGES = ["Io"]


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


def rescan_github():
    for repository in fetch_repositories():
        print repository
