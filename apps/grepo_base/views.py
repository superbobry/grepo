# -*- coding: utf-8 -*-

from __future__ import absolute_import

import re
import textwrap

from annoying.decorators import ajax_request
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404

from .models import Repository


def render(data):
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
    if not request.GET.get("language"):
        return HttpResponseBadRequest()

    language = request.GET["language"].title()
    keywords = request.GET.getlist("keywords")
    limit = request.GET.get("limit", 20)

    repositories = Repository.objects.filter(
        languages__name__iexact=language,
        summary__regex=r"|".join(map(re.escape, keywords))
    ).values_list(
        "name", "url", "languages__name", "score", "summary")[:limit]

    return {"repositories": map(render, repositories)}
