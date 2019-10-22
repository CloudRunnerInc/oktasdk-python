import time
import warnings

from okta.framework.ApiClient import ApiClient
from okta.framework.PagedResults import PagedResults


class SystemLogClient(ApiClient):

    def __init__(self, base_url, api_token, **kwargs):
        super(SystemLogClient, self).__init__(
            base_url + '/api/v1/logs',
            api_token,
            **kwargs
        )

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
        if url:  # pragma: no cover
            assert since is None
            assert until is None
            assert q is None
            assert filter is None
            assert limit is None
            warnings.warn("Don't pass `url`, use `get_next_page` method instead", DeprecationWarning)
            return self.get_next_page(url)

        params = {
            'since': since,
            'until': until,
            'q': q,
            'filter': filter,
            'limit': limit,
        }
        response = self.get_path('/', params=params)
        return PagedResults(response)

    def get_next_page(self, url):
        return PagedResults(self.get(url))

    def get_all_log_event_pages(self, since=None, until=None, q=None, filter=None, limit=None):
        # NOTE: The `sleep_between_pages` argument is removed.
        # Just do whatever you have to do (sleep, yield to event loop, etc) when iterating.
        page = self.get_paged_log_events(
            since=since,
            until=until,
            q=q,
            filter=filter,
            limit=limit,
        )
        yield page.result

        while not page.is_last_page():
            page = self.get_next_page(page.next_url)
            if not page.result:
                return
            yield page.result

    def get_all_log_events(self, since=None, until=None, q=None, filter=None,
                           max_results=None, sleep_between_pages=None, per_page=1000):
        limit = per_page
        if max_results and max_results < limit:
            limit = max_results

        event_count = 0
        for event_list in self.get_all_log_event_pages(
            since=since,
            until=until,
            q=q,
            filter=filter,
            limit=limit,
        ):
            for event in event_list:
                yield event
                event_count += 1
                if max_results is not None and event_count >= max_results:
                    return
            if sleep_between_pages:
                # Consider deprecating this?
                time.sleep(sleep_between_pages)
