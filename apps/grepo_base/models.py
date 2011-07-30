# -*- coding: utf-8 -*-
"""
    grepo_base.models
    ~~~~~~~~~~~~~~~~~

    Model definitions for `grepo`.
"""

from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify


#: Available repository sources, should be populated on the fly, from
#: ``settings.GREPO_BACKENDS`` variable.
SOURCES = [(0, "github.com"),
           (1, "launchpad.net")]


class Language(models.Model):
    name = models.CharField(_("name"), max_length=80)
    slug = models.CharField(_("slug"), max_length=40, blank=True)

    class Meta:
        verbose_name = _("language")
        verbose_name_plural = _("languages")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()

        if not self.slug:
            self.slug = slugify(self.name)

        super(Language, self).save(*args, **kwargs)


class Repository(models.Model):
    url = models.URLField(_("url"), max_length=255)
    name = models.CharField(_("name"), max_length=255)
    score = models.FloatField(_("score"), max_length=255,
        help_text=_("`grepo` score for this repository, the bigger the "
                    "value -- the more help is needed."))
    source = models.SmallIntegerField(_("source"), choices=SOURCES)
    languages = models.ManyToManyField(Language, related_name="repositories")
    summary = models.TextField(_("summary"), blank=True, null=True,
        help_text=_("project summary, to help the users find what they"
                     "want."))
    created_at = models.DateTimeField(_("created"))
    updated_at = models.DateTimeField(_("updated"))

    class Meta:
        verbose_name = _("repository")
        verbose_name_plural = _("repositories")

    def __unicode__(self):
        return self.url

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        super(Repository, self).save(*args, **kwargs)
