# -*- coding: utf-8 -*-
"""Provide application initialization function."""

import os
import time

from flask import Flask, jsonify, send_from_directory, render_template ,request
from .helpers.config import apply_config
from .helpers.mysql import DB as APP_DB


def create_app(config='product'):
    """Create application from config."""
    app = Flask(__name__)
    apply_config(app, config)

    APP_DB.init_app(app)

    from .api.upload import upload
    app.add_url_rule('/upload', 'upload', upload)

    from .api.downtime import downtime
    app.add_url_rule('/downtime', 'downtime', downtime)

    from .api.cron import cron_nodata
    app.add_url_rule('/cron-nodata', 'cron_nodata', cron_nodata)

    from .api.report import report, get_report
    app.add_url_rule('/report', 'report', report)

    static = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

    @app.route('/', methods=['GET'])
    def redirect_to_index():
        return render_template(
            'index.html',
            report=get_report(),
            args=request.args,
            now=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        )

    @app.route('/<path:path>', methods=['GET'])
    def static_proxy(path):
        if path == 'index.html':
            return redirect_to_index()
        return send_from_directory(static, path)

    @app.errorhandler(500)
    def custom500(error):
        response = jsonify({'success': False, 'error': error.description})
        response.status_code = 500
        return response

    return app
