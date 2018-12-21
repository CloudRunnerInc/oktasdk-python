import json

from okta.framework.ApiClient import ApiClient


class SystemLogClient(ApiClient):

    def __init__(self, base_url, api_token):
        ApiClient.__init__(self, base_url + '/api/v1/logs', api_token)

    # CRUD

    def get_log_events(self, since=None, until=None, q=None, filter=None, limit=None):
        """Get a list of log events in JSON format

        :param since: filters the lower time bound of the log events published property
        :type since: datetime or None
        :param until: filters the upper time bound of the log events published property
        :type until: datetime or None
        :param filter: filter expression that filters the results
        :type filter: str or None
        :param q: filters the log events results by one or more exact keywords
        :type q: str or None
        :rtype: list of dictionaries representing log events
        :param limit: The number of results returned in the response
        :type limit: int or None
        """
        params = {
            'since': since,
            'until': until,
            'q': q,
            'filter': filter,
            'limit': limit,
        }
        response = ApiClient.get_path(self, '/', params=params)
        return json.loads(response.text)
