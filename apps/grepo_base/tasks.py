# -*- coding: utf-8 -*-

from __future__ import absolute_import

import time
from datetime import timedelta

from celery.decorators import periodic_task, task

from grepo_base.backends import get_backends
from grepo_base.models import Repository


@task
def update_backend(backend):
    for data in backend:
        r = Repository.objects.get_or_create(url=data["url"])
        [setattr(r, k, v) for k, v in data.itertitems()]
        r.save()

        if hasattr(backend, "delay"):
            time.sleep(backend.delay)


@periodic_task(run_every=timedelta(days=1))
def update_world():
    """Update **all** repositories for **all** backends."""
    for backend in get_backends():
        update_backend.apply_async(backend)
