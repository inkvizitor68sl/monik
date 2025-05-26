# -*- coding: utf-8 -*-
"""Provide helper for MySQL connection."""

import MySQLdb
from flask import g

class MySQL(object):
    """MySQL Flask adapter."""

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app):
        """Initialize application."""
        self.app = app
        self.app.config.setdefault('MYSQL_USER', None)
        self.app.config.setdefault('MYSQL_PASSWORD', None)
        self.app.config.setdefault('MYSQL_HOST', 'localhost')
        self.app.config.setdefault('MYSQL_DB', None)
        self.app.config.setdefault('MYSQL_PORT', 3306)
        self.app.config.setdefault('MYSQL_UNIX_SOCKET', None)
        self.app.config.setdefault('MYSQL_CONNECT_TIMEOUT', 10)
        self.app.config.setdefault('MYSQL_READ_DEFAULT_FILE', None)
        self.app.config.setdefault('MYSQL_USE_UNICODE', True)
        self.app.config.setdefault('MYSQL_CHARSET', 'utf8')
        self.app.config.setdefault('MYSQL_SQL_MODE', None)
        self.app.config.setdefault('MYSQL_CURSORCLASS', None)

        app.teardown_appcontext(self.teardown_request)

    @property
    def connect(self):
        """Return a MySQLdb connection."""
        kwargs = {}
        cfg = self.app.config

        if cfg['MYSQL_HOST']:
            kwargs['host'] = cfg['MYSQL_HOST']
        if cfg['MYSQL_USER']:
            kwargs['user'] = cfg['MYSQL_USER']
        if cfg['MYSQL_PASSWORD']:
            kwargs['passwd'] = cfg['MYSQL_PASSWORD']
        if cfg['MYSQL_DB']:
            kwargs['db'] = cfg['MYSQL_DB']
        if cfg['MYSQL_PORT']:
            kwargs['port'] = cfg['MYSQL_PORT']
        if cfg['MYSQL_UNIX_SOCKET']:
            kwargs['unix_socket'] = cfg['MYSQL_UNIX_SOCKET']
        if cfg['MYSQL_CONNECT_TIMEOUT']:
            kwargs['connect_timeout'] = cfg['MYSQL_CONNECT_TIMEOUT']
        if cfg['MYSQL_READ_DEFAULT_FILE']:
            kwargs['read_default_file'] = cfg['MYSQL_READ_DEFAULT_FILE']
        if cfg['MYSQL_USE_UNICODE']:
            kwargs['use_unicode'] = cfg['MYSQL_USE_UNICODE']
        if cfg['MYSQL_CHARSET']:
            kwargs['charset'] = cfg['MYSQL_CHARSET']
        if cfg['MYSQL_SQL_MODE']:
            kwargs['sql_mode'] = cfg['MYSQL_SQL_MODE']
        if cfg['MYSQL_CURSORCLASS']:
            from MySQLdb import cursors
            kwargs['cursorclass'] = getattr(cursors, cfg['MYSQL_CURSORCLASS'])

        connect = MySQLdb.connect(**kwargs)
        connect.autocommit(True)
        return connect

    @property
    def database(self):
        """Return mysql database."""
        if not hasattr(g, 'mysql_db'):
            g.mysql_db = self.connect
        return g.mysql_db

    def teardown_request(self, exception):
        """Close the DB connection at request end."""
        db = g.pop('mysql_db', None)
        if db is not None:
            db.close()

DB = MySQL()
