# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.contrib import admin

from .models import Language, Repository


admin.site.register(Repository)
admin.site.register(Language)
