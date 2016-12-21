# -*- coding: utf-8 -*-
"""Provide database model for check list."""


from . import APP_DB


class CheckList(object):
    """Provide database checks."""
    def __init__(self):
        self.db = APP_DB.database

    def update_nodata(self):
        """Update status to NO-DATA."""
        cursor = self.db.cursor()
        cursor.execute('''
             UPDATE checks
             SET status=2, description="NODATA"
             WHERE update_date + ttl < NOW() AND downtime_till < NOW();
        ''')

    def get_nodata(self):
        """Get a list of checks with nodata."""
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT * FROM checks
            WHERE update_date + ttl < NOW() AND downtime_till < NOW();
        ''')

        return self._to_dict(
            cursor.fetchall(),
            {'description': 'NO DATA', 'status': 2}
        )

    def get_critical(self, hostname=None, checkname=None):
        """Return a list of critical checks."""
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT * FROM checks
            WHERE downtime_till < NOW() AND status > 0
                AND notify_types LIKE '%%phone%%'
                AND hostname LIKE %(hostname)s
                AND checkname LIKE %(checkname)s
            ORDER BY status DESC, hostname, checkname
        ''', {
            'hostname': '%' if hostname is None \
            else self.db.escape_string(hostname.replace('*', '%')),
            'checkname': '%' if checkname is None \
            else self.db.escape_string(checkname.replace('*', '%'))
        })

        return self._to_dict(cursor.fetchall())

    def get_all(self, hostname=None, checkname=None):
        """Return a list of all check, filtered by checkname and hostname."""
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT * FROM checks
            WHERE hostname LIKE %(hostname)s AND checkname LIKE %(checkname)s
            ORDER BY status DESC, hostname, checkname
        ''', {
            'hostname': '%' if hostname is None \
            else self.db.escape_string(hostname.replace('*', '%')),
            'checkname': '%' if checkname is None \
            else self.db.escape_string(checkname.replace('*', '%'))
        })

        return self._to_dict(cursor.fetchall())

    def _to_dict(self, options, rewrite=None):
        """Simplify dictionary options"""
        if not rewrite:
            rewrite = {}

        if not options:
            return None

        kwargs = []
        for option in options:
            arg = {}
            for key, value in option.items():
                arg[key] = str(value)
                if key in rewrite:
                    arg[key] = rewrite[key]
            kwargs.append(arg)

        return kwargs
