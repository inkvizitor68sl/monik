# -*- coding: utf-8 -*-
"""Provide helper for configure application."""


class BaseConfig(object):
    """Provide basic configuration options."""
    DEBUG = False
    TESTING = False

    MYSQL_CURSORCLASS = 'DictCursor'


class DevelopmentConfig(BaseConfig):
    """Provide developers configuration options."""
    DEBUG = True
    TESTING = False


class ProductionConfig(BaseConfig):
    """Production configuration options."""
    DEBUG = False
    TESTING = False


CONFIG = {
    'product': 'monik.helpers.config.ProductionConfig',
    'develop': 'monik.helpers.config.DevelopmentConfig'
}


def apply_config(app, config):
    """Apply configuration to a given application."""
    app.config.from_object(CONFIG[config])
    app.config.from_envvar('MONIK_SETTINGS', silent=True)
