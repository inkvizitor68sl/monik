# -*- coding: utf-8 -*-
"""Provide database model for check."""

from . import APP_DB


class Check(object):
    """Provide database check model."""

    DEFAULTS = {
        'hostname': '',
        'checkname': '',
        'status': 0,
        'description': '',
        'ttl': 0,
        'ignorenodata': 0,
        'notify_types': ''
    }

    def __init__(self):
        self.db = APP_DB.database

    def find_one(self, host, checkname):
        """Find one check by given host and check name."""
        cursor = self.db.cursor()
        cursor.execute(
            'SELECT * FROM checks WHERE hostname = %s and checkname = %s',
            (self.db.escape_string(host), self.db.escape_string(checkname))
        )
        result = cursor.fetchone()
        return result

    def create_update(self, params):
        """Create new check or update existed."""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO checks
                (hostname, checkname, status, description,
                 ttl, ignorenodata, notify_types, downtime_till)
            VALUES
                (%(hostname)s, %(checkname)s, %(status)s, %(description)s,
                 %(ttl)s, %(ignorenodata)s, %(notify_types)s, NOW())
            ON DUPLICATE KEY UPDATE
                hostname=%(hostname)s, checkname=%(checkname)s,
                status=%(status)s, description=%(description)s,
                ttl=%(ttl)s, ignorenodata=%(ignorenodata)s,
                notify_types=%(notify_types)s, update_date=NOW(),
                downtime_till=NOW();
        ''', self.escape_args(params))

    def update_downtime(self, host, checkname, downtime):
        """Update downtime for current checkname."""
        cursor = self.db.cursor()
        cursor.execute('''
            UPDATE checks
            SET downtime_till = TIMESTAMPADD(SECOND, %(downtime_till)s, NOW())
            WHERE hostname=%(hostname)s AND checkname=%(checkname)s
        ''', self.escape_args({
            'downtime_till': 0 if int(downtime) < 0 else int(downtime),
            'hostname': host,
            'checkname': checkname
        }))

    def escape_args(self, params):
        """Escape all values in dictionary values."""
        result = {}
        for key, value in params.items():
            result[key] = self.db.escape_string(value) \
                    if isinstance(value, (str, unicode)) else value
        return result
