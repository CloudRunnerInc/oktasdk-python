from okta.framework.ApiClient import ApiClient
from okta.framework.PagedResults import PagedResults
import time


class SystemLogClient(ApiClient):

    def __init__(self, base_url, api_token):
        ApiClient.__init__(self, base_url + '/api/v1/logs', api_token)

    # CRUD

    def get_paged_log_events(self, since=None, until=None, q=None, filter=None, limit=None, url=None):
        """Get a paged list of log events

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
        :param url: url that returns a list of log events
        :type url: str
        :rtype: PagedResults of log events in JSON format
        """
        if url:
            response = ApiClient.get(self, url)
        else:
            params = {
                'since': since,
                'until': until,
                'q': q,
                'filter': filter,
                'limit': limit,
            }
            response = ApiClient.get_path(self, '/', params=params)
        return PagedResults(response)

    def get_all_log_event_pages(self, since=None, until=None, q=None, filter=None, limit=None, sleep_between_pages=None):
        page = self.get_paged_log_events(
            since=since,
            until=until,
            q=q,
            filter=filter,
            limit=limit,
        )
        yield page.result

        while not page.is_last_page():
            if sleep_between_pages:
                time.sleep(sleep_between_pages)
            page = self.get_paged_log_events(url=page.next_url)
            yield page.result

    def get_all_log_events(self, since=None, until=None, q=None, filter=None, max_results=None, sleep_between_pages=None):
        limit = 1000
        if max_results and max_results < limit:
            limit = max_results

        i = 0
        for event_list in self.get_all_log_event_pages(
            since=since,
            until=until,
            q=q,
            filter=filter,
            limit=limit,
            sleep_between_pages=sleep_between_pages
        ):
            for event in event_list:
                yield event
                i += 1
                if max_results is not None and i == max_results:
                    raise StopIteration
