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

    .. function:: needs_update(repository)

       Returns ``True`` if a given :class:`~grepo_base.models.Repository`
       instance needs to be updated and ``False`` otherwise.
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import memoize
from django.utils.importlib import import_module


def load_backend(path):
    try:
        module = import_module(path)
    except (ImportError, AttributeError) as e:
        raise ImproperlyConfigured("Error importing Grepo backend {0}: {1}"
                                   .format(path, e))

    for func in ["list", "update"]:
        if not hasattr(module, func):
            raise ImproperlyConfigured(
                "Grepo backend {0} is missing {1}() function."
                .format(module.__name__, func)
            )

    return module

load_backend = memoize(load_backend, {}, 1)


def get_backends():
    return map(load_backend, settings.GREPO_BACKENDS)
