# -*- coding: utf-8 -*-
"""
    grepo_base.models
    ~~~~~~~~~~~~~~~~~

    Model definitions for `grepo`.
"""


from datetime import datetime

from django.db import models
from django.utils.translation import ugettext as _


#: Available repository sources, should be populated on the fly, from
#: ``settings.GREPO_BACKENDS`` variable.
SOURCES = [(0, "github.com"),
           (1, "launchpad.net")]


class Repository(models.Model):
    url = models.CharField(_("url"), max_length=255)
    name = models.CharField(_("name"), max_length=255)
    score = models.FloatField(_("score"), max_length=255,
        help_text=_("`grepo` score for this repository, the bigger the "
                    "value -- the more help is needed."))
    source = models.SmallIntegerField(_("source"), choices=SOURCES)
    created_at = models.DateTimeField(_("created"))
    updated_at = models.DateTimeField(_("updated"))

    def save(self):
        self.update_at = datetime.now()
        super(Repository, self).save()


def calculate_grepo_score():
    """Returns `grepo` score for a bunch of repository metadata."""
    return 0
