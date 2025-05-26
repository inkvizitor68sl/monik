# -*- coding: utf-8 -*-
"""Provide uwsgi-like monitoring application."""

import sys
import importlib

__version__ = '0.1'

if sys.version_info.major < 3:
    importlib.reload(sys)
sys.setdefaultencoding('utf-8')
