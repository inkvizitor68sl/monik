# -*- coding: utf-8 -*-
"""Provide report API."""

from . import flask
from . import CheckListModel


def get_report():
    """Provide report data."""
    try:
        params = _get_report_params(flask.request.args)
        if params['critical']:
            return {
                'success': True,
                'data': _show_critical(
                    params['hostname'], params['checkname']
                )
            }

        return {
            'success': True,
            'data': _show_filter(params['hostname'], params['checkname'])
        }

    except Exception as error:
        flask.abort(500, '{}'.format(error))


def report():
    """Provide report API."""
    return flask.jsonify(get_report())


def _get_report_params(params):
    """Get a report params"""
    kwargs = {
        'critical': None,
        'hostname': None,
        'checkname': None
    }

    for arg in kwargs.keys():
        if params.get(arg, None):
            kwargs[arg] = params[arg]

    return kwargs


def _show_critical(hostname, checkname):
    """Show criticals check events"""
    checks = CheckListModel()
    criticals = checks.get_critical(hostname, checkname)
    if not criticals:
        return "all ok"

    return criticals


def _show_filter(hostname, checkname):
    """Show filtered check events."""
    checks = CheckListModel()
    return checks.get_all(hostname, checkname)
