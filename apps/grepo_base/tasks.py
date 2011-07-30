# -*- coding: utf-8 -*-

from datetime import timedelta

from celery.decorators import periodic_task


@periodic_task(run_every=timedelta(days=1))
def rescan_backends():
    pass
