# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template


urlpatterns = patterns("grepo_base.views",
    url(r"^$", direct_to_template, {"template": "index.html"}),
    url(r"^search/$", "search"),
)
