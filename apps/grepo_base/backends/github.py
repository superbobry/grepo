# -*- coding: utf-8 -*-
"""
    grepo_base.github
    ~~~~~~~~~~~~~~~~~

    Github.com backend for `grepo`.
"""

import itertools
import math
from datetime import datetime
from httplib import HTTPConnection

from dateutil import parser
from django.utils import simplejson as json

from grepo_base.models import Language


#: Github api search path
SEARCH_PATH = "/api/v2/json/repos/search/language:{lang}?start_page={page}"
#: Github host, used for httplib for connect to api
GITHUB = "github.com"
#: Github specify language names
GITHUB_LANGS = {
    'Actionscript': 'ActionScript',
    'Applescript': 'AppleScript',
    'Asp': 'ASP',
    'Coffeescript': 'CoffeeScript',
    'Coldfusion': 'ColdFusion',
    'Lisp': ['"Common Lisp"', '"Emacs Lisp"'],
    'Fortran': 'FORTRAN',
    'Javascript': 'JavaScript',
    'Llvm': 'LLVM',
    'Ocaml': 'OCaml',
    'Ooc': 'ooc',
    'Php': 'PHP',
    'Visual Basic': '"Visual Basic"',
}

GREPO_LANGS = {
    "Common Lisp": "Lisp",
    "Emacs Lisp": "Lisp"
}


parse_gh_datetime = parser.parse


class GithubBackend(object):

    def __init__(self):
        self.response = None
        self.delayed = False

    def fetch(self, language, page):
        connection = HTTPConnection(GITHUB)
        connection.request("GET", SEARCH_PATH.format(lang=language, page=page))
        self.response = connection.getresponse()
        self.data = self.response.read()
        self.delayed = False

    @property
    def delay(self):
        if self.delayed:
            return 0
        self.delayed = True
        remain = int(self.response.getheader("x-ratelimit-remaining"))
        if remain < 4:
            return 4 - remain
        return 0

    def calculate_score(self, updated, project):
        watchers = project["watchers"] or 1
        forks = project["forks"] or 1
        issues = project["open_issues"] or 1

        score = (datetime.utcnow() - updated.replace(tzinfo=None)).days * \
            math.exp(issues / (watchers + forks))
        return score % 365. / 365.

    def iter_for_lang(self, lang):
        for page in itertools.count(1):
            self.fetch(lang, page)
            repositories = json.loads(self.data)["repositories"]

            if not repositories:
                break

            for repository in repositories:
                if (not repository["language"] or
                    repository["fork"] or
                    repository["private"]):
                    continue

                # If there is no "updated_at" field in api output,
                # then repository wasn't ever updated and `updated_at`
                # equals to `created_at`
                updated = repository.get("updated_at",
                                         repository["created_at"])
                updated = parse_gh_datetime(updated)
                created = parse_gh_datetime(repository["created_at"])

                language = GREPO_LANGS.get(repository["language"].title(),
                                           repository["language"].title())
                languages = [language]
                yield {
                    "url": repository["url"],
                    "name": repository["name"],
                    "languages": languages,
                    "score": self.calculate_score(updated, repository),
                    "summary": repository.get("description", ""),
                    "updated_at": updated,
                    "created_at": created
                }

    def __iter__(self):
        """Yields all repositories one by one."""
        for language in Language.objects.all():
            langs = GITHUB_LANGS.get(language.name, language.name)

            if not isinstance(langs, list):
                langs = [langs]

            for lang in langs:
                for repository in self.iter_for_lang(lang):
                    yield repository
