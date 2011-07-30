# -*- coding: utf-8 -*-
"""
    grepo_base.backends
    ~~~~~~~~~~~~~~~~~~~

    Each backend is expected to define **at least** the ``__iter__``
    function, yielding repository data dicts, suitable for passing
    directly to :class:`~grepo_base.models.Repository` constructor.
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
            "Grepo backend {0} is missing '__iter__' method."
            .format(backend.__name__)
        )
    else:
        return backend

load_backend = memoize(load_backend, {}, 1)


def get_backends():
    return map(load_backend, settings.GREPO_BACKENDS)
