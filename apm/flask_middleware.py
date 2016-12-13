# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import re
import logging
from datetime import datetime

import werkzeug

from .aggregator import Aggregator


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class FlaskMiddleware(object):
    def __init__(self, app):
        import flask
        from flask import request
        if not isinstance(app, flask.Flask):
            raise RuntimeError('FlaskMiddleware must accept flask app as first parameter')
        import leancloud
        if leancloud.__version__ < '1.8.0':
            raise RuntimeError('TODO')
        self.aggregator = Aggregator('request', 60)
        self.aggregator.start()

        @app.before_request
        def before_flask_request():
            request.environ['_LEANENGINE_APM_FLASK_REQUEST_URL_RULE'] = request.url_rule
        self.app = app

    def __call__(self, environ, start_response):
        start = datetime.now()
        request = werkzeug.Request(environ, shallow=True)

        def new_start_response(status, headers, **kwargs):
            url_rule = environ['_LEANENGINE_APM_FLASK_REQUEST_URL_RULE']
            elapsed = datetime.now() - start
            matched = re.findall('.*\.(css|js|jpe?g|gif|png|woff2?|ico)$', request.path)
            if request.method == 'GET' and matched:
                url = 'GET *.%s' % matched[0]
            else:
                url = '%s %s' % (request.method, url_rule)
            data = {
                'count': 1,
                'responseTime': elapsed.total_seconds() * 1000,
                'url': url,
                'method': request.method,
            }
            try:
                status_code = status.split()[0]
                status_code = int(status_code)
                data['statusCode'] = status_code
                self.aggregator.put(data)
            except Exception as e:
                logger.warn('parse status code error: %s', e)
            return start_response(status, headers, **kwargs)
        return self.app(environ, new_start_response)
