# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .models import Language

def grepo(request):
    """Adds grepo-related context variables to the context."""
    return {
        "GREPO_LANGUAGES": Language.objects.all().values_list("name", flat=True)
    }
