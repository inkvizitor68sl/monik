# -*- coding: utf-8 -*-
"""Provide downtime API."""

from . import flask
from . import CheckModel


def downtime():
    """Provide downtime api logic."""
    params = _get_downtime_params(flask.request.headers)

    check = CheckModel()
    current_check = check.find_one(params['hostname'], params['checkname'])

    if not current_check:
        flask.abort(
            500,
            'Check {checkname} for host {hostname} not exists'.format(
                **params
            )
        )

    try:
        check.update_downtime(
            params['hostname'],
            params['checkname'],
            params['downtime_secs']
        )
    except Exception as error:
        flask.abort(500, '{}'.format(error))

    return flask.jsonify({'success': True})


def _get_downtime_params(search):
    """Proceed downtime params."""
    kwargs = {}
    args = ('hostname', 'checkname', 'downtime_secs')

    for key, value in search:
        arg = key.replace('-', '_').lower().strip()
        if arg in args:
            kwargs[arg] = value
    if set(kwargs.keys()) != set(args):
        flask.abort(500, 'Params {} required!'.format(', '.join(args)))

    return kwargs
