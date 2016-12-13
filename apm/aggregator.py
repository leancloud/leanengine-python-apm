# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import time
import copy
import socket
import logging
import threading

import requests


token = None
url = os.environ.get('APM_URL_PREFIX', 'http://apm.leanapp.cn') + '/metrics'
instance = os.environ.get('LEANCLOUD_APP_INSTANCE', socket.gethostname())
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Buffer(object):
    pass


class Aggregator(object):
    def __init__(self, name, interval):
        self.name = name
        self.interval = interval
        self.lock = threading.Lock()
        self.buffer = {}
        self.thread = threading.Thread(target=self.run)
        self.session = requests.Session()

    def put(self, data):
        with self.lock:
            if len(self.buffer) > 10000:
                logger.warn('Aggregator.buffer\'s size is up to 10000, ignore new metrics')
                return
            key = (data['url'], data['statusCode'])
            if key in self.buffer:
                self._merge_response_time(key, data)
            else:
                self.buffer[key] = data

    def _merge_response_time(self, key, new):
        current = self.buffer[key]
        result_total = current['responseTime'] * current['count'] + new['responseTime'] * new['count']
        result_count = current['count'] + new['count']
        current['responseTime'] = result_total / result_count
        current['count'] = result_count

    def run(self):
        while True:
            time.sleep(self.interval)
            self.send_metrics()

    def start(self):
        return self.thread.start()

    def send_metrics(self):
        with self.lock:
            if not self.buffer:
                return
            buffer = copy.copy(self.buffer)
            self.buffer = {}
            headers = {
                'Authorization': token,
            }
            data = {
                'instance': instance,
                'metric': self.name,
                'points': list(buffer.values()),
            }
            logger.info('send APM metrics, count: %d', len(buffer))
            try:
                response = self.session.post(url, json=data, headers=headers)
            except Exception as e:
                logger.warn('send_metrics error: %s', e)
                return
            if not response.ok:
                logger.warn('send_metrics error: %s %s', response.status_code, response.content)


def init(_token):
    global token
    token = _token
