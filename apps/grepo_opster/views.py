# -*- coding: utf-8 -*-

import random
from cStringIO import StringIO

import opster
from annoying.decorators import ajax_request
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET


# Monkey patching `opster` to use **our** sysname, not just `manage.py`.
opster.sysname = lambda *args: settings.GREPO_NAME


@opster.command(options=settings.GREPO_OPTIONS,
                usage=settings.GREPO_USAGE)
def stub(*args, **kwargs):
    """A stub command, validating `grepo` input, why? because all of
    the JavaScript implementation are either heavily Node.js-based or
    simply not usable.
    """
    language = kwargs["language"]
    if language not in settings.GREPO_LANGUAGES:
        raise opster.Abort(
            "sorry, grepo doesn't speak {0!r}, how about: {1!r}?"
            .format(language, random.choice(settings.GREPO_LANGUAGES)))


@require_GET
@csrf_exempt
@ajax_request
def parse(request):
    stdout = StringIO()
    stderr = StringIO()

    # Monkey-patching `opster` to work with our stdout and stderr
    # streams.
    opster.write.func_defaults = (stdout, )
    opster.err = lambda text: opster.write(text, out=stderr)

    stub(argv=request.GET.getlist("argv[]"))

    return {"stderr": stderr.getvalue(),
            "stdout": stdout.getvalue()}
