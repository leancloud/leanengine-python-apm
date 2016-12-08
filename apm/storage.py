# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json

from six.moves import urllib

from .aggregator import Aggregator


def make_request_hook(aggregator):
    def request_hook(response, *args, **kwargs):
        url = urllib.parse.urlparse(response.url)
        splits = url.path.split('/')
        if splits[2] != 'classes':
            return

        aggregator.put({
            'count': 1,
            'responseTime': response.elapsed.total_seconds() * 1000,
            'statusCode': response.status_code,
            'method': response.request.method,
            'url': generate_url(response.request),
        })
    return request_hook


def generate_url(request):
    parsed = urllib.parse.urlparse(request.url)
    splits = parsed.path.split('/')
    method = request.method
    class_name = splits[3]
    url = '%s classes/%s' % (method, class_name)
    if is_get_request(parsed.query):
        url += '/:id'
    return url


def is_get_request(query):
    if not query:
        return False
    qs = urllib.parse.parse_qs(query)
    if not qs.get('where'):
        return False
    where = json.loads(qs['where'][0])
    return where.get('objectId') is not None


def install():
    import leancloud
    if leancloud.__version__ < '1.8.0':
        raise RuntimeError('TODO')
    aggregator = Aggregator('cloudApi', 60)
    leancloud.client.request_hooks['response'] = make_request_hook(aggregator)
    aggregator.start()
