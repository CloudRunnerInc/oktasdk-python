import requests
import json
import time
from okta.framework.Serializer import Serializer
from okta.framework.OktaError import OktaError
import six
from six.moves.urllib.parse import urlencode


def dict_to_query_params(d):
    if d is None or len(d) == 0:
        return ""

    return "?{}".format(urlencode({
        param: str(value).lower() if type(value) == bool else str(value)
        for param, value in six.iteritems(d) if value is not None
    }))


class ApiClient(object):
    def __init__(self, base_url, api_token, max_attempts=1):
        self.base_url = base_url
        self.api_token = api_token
        self.api_version = 1
        self.max_attempts = max_attempts

        if not self.base_url:
            raise ValueError('Invalid base_url')

        if not self.api_token:
            raise ValueError('Invalid api_token')

        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'SSWS ' + api_token
        }

    def _request(self, request_func, *args, **kwargs):
        max_attempts = kwargs.pop("attempts", None)
        if max_attempts is None:
            max_attempts = self.max_attempts
        max_attempts = max(1, max_attempts)

        attempt = 1
        while True:
            resp = request_func(*args, **kwargs)
            if resp is None:
                raise ValueError("A response wasn't received")
            if 200 <= resp.status_code < 300:
                return resp
            if attempt >= max_attempts or resp.status_code != 429:
                error_data = resp.json()
                error_data.update(status_code=resp.status_code)
                raise OktaError(error_data)
            time.sleep(2 ** (attempt - 1))

    def get(self, url, params=None, max_attempts=None):
        params_str = dict_to_query_params(params)
        return self._request(
            requests.get,
            url + params_str,
            headers=self.headers,
            attempts=max_attempts
        )

    def put(self, url, data=None, params=None, attempts=None):
        d = json.dumps(data, cls=Serializer)
        params_str = dict_to_query_params(params)
        return self._request(
            requests.put,
            url + params_str,
            data=d,
            headers=self.headers,
            attempts=attempts,
        )

    def post(self, url, data=None, params=None, attempts=None):
        d = json.dumps(data, cls=Serializer)
        params_str = dict_to_query_params(params)
        return self._request(
            requests.post,
            url + params_str,
            data=d,
            headers=self.headers,
            attempts=attempts,
        )

    def delete(self, url, params=None, attempts=None):
        params_str = dict_to_query_params(params)
        return self._request(
            requests.delete,
            url + params_str,
            headers=self.headers,
            attempts=attempts,
        )

    def get_path(self, url_path, params=None):
        return self.get(self.base_url + url_path, params=params)

    def put_path(self, url_path, data=None, params=None):
        return self.put(self.base_url + url_path, data=data, params=params)

    def post_path(self, url_path, data=None, params=None):
        return self.post(self.base_url + url_path, data=data, params=params)

    def delete_path(self, url_path, params=None):
        return self.delete(self.base_url + url_path, params=params)
