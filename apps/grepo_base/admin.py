# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.contrib import admin
from django.utils.translation import ugettext as _
from django.template.defaultfilters import urlize

from .models import Language, Repository


class RepositoryAdmin(admin.ModelAdmin):
    list_filter = ["languages", "updated_at"]
    list_display = ["name", "url_with_link", "all_languages", "score",
                    "updated_at"]
    list_per_page = 25
    list_select_related = True

    search_fields = ["language__name", "name", "summary", "url"]

    def url_with_link(self, instance):
        return urlize(instance.url)
    url_with_link.short_description = _("URL")
    url_with_link.allow_tags = True

    def all_languages(self, instance):
        return ", ".join(map(unicode, instance.languages.all()))
    all_languages.short_description = _("languages")


admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Language)
