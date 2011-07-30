# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns("",
    url(r"^$", include("grepo_base.urls")),
    url(r"^admin/", include(admin.site.urls)),
)
