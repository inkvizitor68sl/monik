# -*- coding: utf-8 -*-
"""Provide helper for MySQL connection."""

from __future__ import absolute_import
import MySQLdb

try:
    from flask import _app_ctx_stack as _ctx_stack
except ImportError:
    from flask import _request_ctx_stack as _ctx_stack


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

        # Flask 0.9 or later
        if hasattr(app, 'teardown_appcontext'):
            self.app.teardown_request(self.teardown_request)
        # Flask 0.7 to 0.8
        elif hasattr(app, 'teardown_request'):
            self.app.teardown_request(self.teardown_request)
        # Older versions
        else:
            self.app.after_request(self.teardown_request)

    @property
    def connect(self):
        """Return a MySQLdb connection."""
        kwargs = {}
        if self.app.config['MYSQL_HOST']:
            kwargs['host'] = self.app.config['MYSQL_HOST']

        if self.app.config['MYSQL_USER']:
            kwargs['user'] = self.app.config['MYSQL_USER']

        if self.app.config['MYSQL_PASSWORD']:
            kwargs['passwd'] = self.app.config['MYSQL_PASSWORD']

        if self.app.config['MYSQL_DB']:
            kwargs['db'] = self.app.config['MYSQL_DB']

        if self.app.config['MYSQL_PORT']:
            kwargs['port'] = self.app.config['MYSQL_PORT']

        if self.app.config['MYSQL_UNIX_SOCKET']:
            kwargs['unix_socket'] = self.app.config['MYSQL_UNIX_SOCKET']

        if self.app.config['MYSQL_CONNECT_TIMEOUT']:
            kwargs['connect_timeout'] = \
                self.app.config['MYSQL_CONNECT_TIMEOUT']

        if self.app.config['MYSQL_READ_DEFAULT_FILE']:
            kwargs['read_default_file'] = \
                self.app.config['MYSQL_READ_DEFAULT_FILE']

        if self.app.config['MYSQL_USE_UNICODE']:
            kwargs['use_unicode'] = self.app.config['MYSQL_USE_UNICODE']

        if self.app.config['MYSQL_CHARSET']:
            kwargs['charset'] = self.app.config['MYSQL_CHARSET']

        if self.app.config['MYSQL_SQL_MODE']:
            kwargs['sql_mode'] = self.app.config['MYSQL_SQL_MODE']

        if self.app.config['MYSQL_CURSORCLASS']:
            from MySQLdb import cursors
            kwargs['cursorclass'] = getattr(
                cursors, self.app.config['MYSQL_CURSORCLASS']
            )

        connect = MySQLdb.connect(**kwargs)
        connect.autocommit(True)
        return connect

    @property
    def database(self):
        """Return mysql database."""
        ctx = _ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, "mysql_db"):
                ctx.mysql_db = self.connect
            return ctx.mysql_db

    def teardown_request(self, exception):
        """Close on request close connection."""
        ctx = _ctx_stack.top
        if hasattr(ctx, "mysql_db"):
            ctx.mysql_db.close()

DB = MySQL()
