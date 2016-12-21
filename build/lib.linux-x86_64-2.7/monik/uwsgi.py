# -*- coding: utf-8 -*-
"""Provide uwsgi interface for application."""

import os
from .app import create_app

app = create_app(os.getenv('MONIK_CONFIG', 'product'))
