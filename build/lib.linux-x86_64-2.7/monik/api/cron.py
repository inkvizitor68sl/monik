# -*- coding: utf-8 -*-
"""Provide cron API."""

from . import flask
from . import CheckListModel
from . import Command


def cron_nodata():
    try:
        checks = CheckListModel()
        nodata = checks.get_nodata()
        if not nodata:
            return flask.jsonify({'success': True})

        checks.update_nodata()

        cmd = Command(flask.current_app.config)
        for item in nodata:
            cmd.run(item)
    except Exception as error:
        flask.abort(500, '{}'.format(error))

    return flask.jsonify({'success': True})
