# -*- coding: utf-8 -*-
"""
    grepo_opster.views
    ~~~~~~~~~~~~~~~~~~

    This module implements a tiny wrapper around :mod:`opster` for
    validating `grepo` input, why? because all of the JavaScript
    implementation are either heavily Node.js-based or simply not
    usable.
"""

import random
from cStringIO import StringIO

import opster
from annoying.decorators import ajax_request
from django.conf import settings
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_GET

from grepo_base.models import Language

# Monkey patching `opster` to use **our** sysname, not just `manage.py`.
opster.sysname = lambda *args: settings.GREPO_NAME


@opster.command(options=settings.GREPO_OPTIONS,
                usage=settings.GREPO_USAGE)
def stub(*args, **kwargs):
    language = kwargs["language"].title()
    if not language:
        raise opster.Abort(
            _("sorry, can't grepo anything without a language :(")
        )
    if not Language.objects\
        .filter(Q(slug=language) | Q(name=language)).exists():
        total = Language.objects.count()

        if total is 1:
            hint = Language.objects.get()
        else:
            hint = Language.objects.get(pk=random.randrange(1, total))

        raise opster.Abort(
            _("sorry, grepo doesn't speak {0}, how about: {1}?")
             .format(language, hint)
        )

    return kwargs


@require_GET
@ajax_request
def parse(request):
    stdout = StringIO()
    stderr = StringIO()

    # Monkey-patching `opster` to work with our stdout and stderr
    # streams.
    opster.write.func_defaults = (stdout, )
    opster.err = lambda text: opster.write(text, out=stderr)

    options = stub(argv=request.GET.getlist("argv[]"))

    return {"options": options,
            "stderr": stderr.getvalue(),
            "stdout": stdout.getvalue()}
