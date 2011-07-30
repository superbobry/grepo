# -*- coding: utf-8 -*-

from __future__ import absolute_import

import re
import textwrap

from annoying.decorators import ajax_request
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET

from .models import Repository


def render(data):
    """Renders a given repository tuple into an ASCII-dialog; tuple
    items are as follows: repository name and url, main programing
    language for this repository, calculated Grepo-score and
    *hopefuly* short project summary.
    """
    data = list(data)

    summary = textwrap.wrap(data.pop(), width=72)
    if len(summary) is 1:
        summary.insert(0, "")

    data.extend(summary)

    return "\n".join([
        "+"         + "-" * 94                                  + "+",
        "| {0:20} " +          "| {1:50}" +   "|" +       "{2:>18} |",
        "| {4:72} " +                         "|                   |",
        "| {5:72} " +                         "| score:  {3: 9.2f} |",
        "+"         + "-" * 94                                  + "+",
    ]).format(*data)


@require_GET
@ajax_request
def search(request):
    """Fetches up to a `limit` repositories for a given `language`
    and returns them ASCII-rendered.
    """
    if not request.GET.get("language"):
        return HttpResponseBadRequest()

    language = request.GET["language"].title()
    keywords = request.GET.getlist("keywords")

    limit = request.GET.get("only", 20)

    repositories = Repository.objects.filter(
        languages__name__iexact=language,
        summary__regex=r"|".join(map(re.escape, keywords))
    ).values_list(
        "name", "url", "languages__name", "score", "summary")[:limit]

    return {"repositories": map(render, repositories)}


if not settings.DEBUG:
    search = cache_page(60 * 15)(search)  # 15 mins should be enough.
