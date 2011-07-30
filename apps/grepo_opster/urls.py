# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("",
    url(r"^$", "grepo_opster.views.parse", name="grepo_opster_parse"),
)
