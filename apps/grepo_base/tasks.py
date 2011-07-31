# -*- coding: utf-8 -*-

from __future__ import absolute_import

import time
from datetime import timedelta

from celery.decorators import periodic_task, task
from django.conf import settings

from grepo_base.backends import load_backend
from grepo_base.models import Language, Repository


@task
def update_backend(backend):
    # Pre-fetch all available languages, since they aren't likely to
    # change anyway.
    backend = load_backend(backend)
    all_languages = dict([(l.name, l) for l in Language.objects.all()])

    for data in backend:
        languages = [all_languages[l] for l in data.pop("languages")]
        try:
            r = Repository.objects.get(url=data["url"])
        except Repository.DoesNotExist:
            r = Repository()

        [setattr(r, k, data[k]) for k in data]

        r.save()

        r.languages.add(*languages)

        if hasattr(backend, "delay"):
            time.sleep(backend.delay)


@periodic_task(run_every=timedelta(days=1))
def update_world():
    """Update **all** repositories for **all** backends."""
    for backend in settings.GREPO_BACKENDS:
        update_backend.delay(backend)
