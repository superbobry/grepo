# -*- coding: utf-8 -*-

from django.conf import settings

def grepo(request):
    """Adds grepo-related context variables to the context."""
    return {"GREPO_LANGUAGES": settings.GREPO_LANGUAGES}
