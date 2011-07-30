# -*- coding: utf-8 -*-
"""
    grepo_base.github
    ~~~~~~~~~~~~~~~~~

    Github.com backend for `grepo`.
"""
import itertools
from httplib import HTTPConnection
from datetime import datetime

from django.conf import settings
from django.utils import simplejson as json

from grepo_base.models import Repository, Language


#: Github api search path
SEARCH_PATH = "/api/v2/json/repos/search/language:{lang}?start_page={page}"
#: Github host, used for httplib for connect to api
GITHUB = "github.com"


def fetch(language, page):
    connection = HTTPConnection(GITHUB)
    connection.request("GET", SEARCH_PATH.format(lang=language, page=page))
    response = connection.getresponse()
    foo = response.read()
    return foo


def list():
    """Yields all repositories one by one."""
    for language in Language.objects.all():
        for page in itertools.count(1):
            data = fetch(language.name, page)
            repositories = json.loads(data)["repositories"]

            if not repositories:
                break

            for repository in repositories:
                if not repository["language"]:
                    continue

                # Note: `source` and `language` field should be handled
                # by the caller.
                yield {
                    "url": repository["url"],
                    "name": repository["name"],
                    "language": repository["language"],
                    "summary": repository["description"],
                    "score": calculate_repository_score(repository),
                    "updated_at": datetime.utcnow(),
                    "created_at": datetime.utcnow()
                }


def update(repository):
    return repository  # A simple pass-through for now.


def calculate_repository_score(data):
    """Calculates and returns Grepo-score for a given repository.

    .. todo:: query for pull requests and add them to the exponent
              argument.
    """
    parse = lambda d: datetime.strptime(d, "%Y/%m/%dT %H:%M:%S %z")

    data.update(
        created_at=parse(data["created_at"]),
        pushed_at=parse(data["pushed_at"])
    )

    return (data["created_at"] - data["pushed_at"]) * math.exp(
        1 / (data["open_issues"] + data["watchers"] / data["forks"])
    )
