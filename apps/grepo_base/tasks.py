# -*- coding: utf-8 -*-

from __future__ import absolute_import

import time
from datetime import timedelta

from celery.decorators import periodic_task, task

from grepo_base.backends import get_backends
from grepo_base.models import Repository, Language


@task
def update_backend(backend):
    # Pre-fetch all available languages, since they aren't likely to
    # change anyway.
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
    for backend in get_backends():
        update_backend.apply_async(args=(backend,))
