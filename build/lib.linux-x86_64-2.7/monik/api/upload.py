# -*- coding: utf-8 -*-
"""Provide upload API."""


from . import flask
from . import CheckModel
from . import Command


def upload():
    """Upload information."""
    params = _get_upload_params(flask.request.headers)
    try:
        check = CheckModel()

        current = check.find_one(params['hostname'], params['checkname'])
        if current:
            params = _update_with_defaults(params, current)
            if str(current['status']) != str(params['status']):
                cmd = Command(flask.current_app.config)
                cmd.run(params)

        check.create_update(_update_with_defaults(params, check.DEFAULTS))

    except Exception as error:
        flask.abort(500, '{}'.format(error))

    return flask.jsonify({'success': True})


def _update_with_defaults(params, defaults):
    for key, value in defaults.items():
        if key not in params:
            params[key] = value
    return params


def _get_upload_params(search):
    """Return a list of params for check."""
    kwargs = {}

    search_fields = CheckModel.DEFAULTS.keys()
    for key, value in search.items():
        field = key.replace('-', '_').lower().strip()
        if field in search_fields:
            kwargs[field] = value

    if not kwargs.get('hostname', None) \
        or not kwargs.get('checkname', None) \
            or not kwargs.get('status', None):
        flask.abort(500, 'Params hostname, checkname, status required!')

    return kwargs
