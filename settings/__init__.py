# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os

from .base import *

if "EPIO" in os.environ:
    from .epio import *
else:
    try:
        from .local import *
    except ImportError:
        pass


import djcelery
djcelery.setup_loader()
