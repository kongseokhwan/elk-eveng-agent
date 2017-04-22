__author__ = 'kongseokhwan'

import json
import requests
from oslo_log import log as logging

LOG = logging.getLogger(__name__)

BASE_URL = 'https://$s:$s/api/v1/namespaces'

class Openwhisk_API():
    def __init__(self, server_ip='127.0.0.1', server_port='8443',
                 base_url=None, timeout=None, rate_limit=True):
        self.Openwhisk_server = server_ip
        self.Openwhisk_port = server_port
        self._timeout = 60000   # 60000 msec
        self.rate_limit = None

        if base_url is None:
            self.base_url = BASE_URL
        else:
            self.base_url = base_url

        self.base_url = self.base_url % (self.Openwhisk_server,
                                         self.Openwhisk_port)

    def _RequestUrl(self, url, verb, data=None, json=None):
        """Request a url.
        Args:
            url:
                The web location we want to retrieve.
            verb:
                Either POST or GET.
            data:
                A dict of (str, unicode) key/value pairs.
        Returns:
            A JSON object.
        """

        if not data:
            data = {}

        if verb == 'POST':
            if data:
                resp = requests.post(url, data=data, timeout=self._timeout)
            elif json:
                resp = requests.post(url, json=json, timeout=self._timeout)
            else:
                resp = 0  # POST request, but without data or json

        elif verb == 'GET':
            resp = requests.get(url, timeout=self._timeout)

        else:
            resp = 0  # if not a POST or GET request

        if url and self.rate_limit:
            limit = resp.headers.get('x-rate-limit-limit', 0)
            remaining = resp.headers.get('x-rate-limit-remaining', 0)
            reset = resp.headers.get('x-rate-limit-reset', 0)

            self.rate_limit.set_limit(url, limit, remaining, reset)

        return resp

    def send_trigger_evnet(self, url, data):
        url = self.base_url + url
        resp = self._RequestUrl(url, verb='POST', data)
        LOG.DEBUG("send_trigger_event : %s, [RESP] %s", data, resp)






