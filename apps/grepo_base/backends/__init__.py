# -*- coding: utf-8 -*-
"""
    grepo_base.backends
    ~~~~~~~~~~~~~~~~~~~

    Each backend is expected to define **at least** the following
    functions:

    .. function:: list()

       Returns an iterable, yielding repository data dicts, suitable for
       passing to :class:`~grepo_base.models.Repository` constructor.

    .. function:: update(repository)

       Updates a given :class:`~grepo_base.models.Repository` object,
       **without** saving it to the database.
"""

from inspect import isgenerator

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import memoize
from django.utils.importlib import import_module


def load_backend(path):
    module_path, obj_name = path.rsplit(".", 1)
    try:
        module = import_module(module_path)
        Backend = getattr(module, obj_name)
    except (ImportError, AttributeError) as e:
        raise ImproperlyConfigured("Error importing Grepo backend {0}: {1}"
                                   .format(path, e))
    backend = Backend()
    if not hasattr(backend, "__iter__"):
        raise ImproperlyConfigured(
                "Grepo backend {0} disabled.".format(path)
        )
    return backend

load_backend = memoize(load_backend, {}, 1)


def get_backends():
    return map(load_backend, settings.GREPO_BACKENDS)
