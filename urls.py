# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns("",
    url(r"^$", direct_to_template, {"template": "index.html"}),
    url(r"^opster/$", include("grepo_opster.urls")),
    url(r"^admin/", include(admin.site.urls)),
) + staticfiles_urlpatterns()
