# -*- coding: utf-8 -*-
"""
    grepo_base.github
    ~~~~~~~~~~~~~~~~~

    Github.com backend for `grepo`.
"""

import itertools

from httplib import HTTPConnection
from dateutil import parser

from django.utils import simplejson as json

from grepo_base.models import Language


#: Github api search path
SEARCH_PATH = "/api/v2/json/repos/search/language:{lang}?start_page={page}"
#: Github host, used for httplib for connect to api
GITHUB = "github.com"


parse_gh_datetime = parser.parse


class GithubBackend(object):

    def __init__(self):
        self.response = None

    def fetch(self, language, page):
        connection = HTTPConnection(GITHUB)
        connection.request("GET", SEARCH_PATH.format(lang=language, page=page))
        self.response = connection.getresponse()
        self.data = self.response.read()

    def __iter__(self):
        """Yields all repositories one by one."""
        for language in Language.objects.all():
            for page in itertools.count(1):
                self.fetch(language.name, page)
                repositories = json.loads(self.data)["repositories"]

                if not repositories:
                    break

                for repository in repositories:
                    if not repository["language"]:
                        continue

                    # Note: `source` and `language` field should be handled
                    # by the caller.

                    created = parse_gh_datetime(repository["created_at"])
                    # If there is no "updated_at" field in api output,
                    # then repository wasn't ever updated and `updated_at`
                    # equals to `created_at`
                    updated = repository.get("updated_at",
                                             repository["created_at"])
                    updated = parse_gh_datetime(updated)
                    out = {
                        "url": repository["url"],
                        "name": repository["name"],
                        "language": repository["language"],
                        "summary": repository.get("description", ""),
                        "updated_at": updated,
                        "created_at": created,
                        "open_issues": repository["open_issues"],
                        "watchers": repository["watchers"],
                        "forks": repository["forks"],
                        "score": repository["score"]
                    }
                    yield out
