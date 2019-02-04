from okta.framework.ApiClient import ApiClient
from okta.framework.Utils import Utils
from okta.models.event.Event import Event
from okta.framework.PagedResults import PagedResults


class EventsClient(ApiClient):
    def __init__(self, base_url, api_token, **kwargs):
        super(EventsClient, self).__init__(
            base_url + '/api/v1/events',
            api_token,
            **kwargs
        )

    def get_events(self, limit=None, start_date=None, filter_string=None):
        """Get a list of Events

        :param limit: maximum number of events to return
        :type limit: int or None
        :param filter_string: string to filter events
        :type filter_string: str or None
        :rtype: list of Event
        """
        params = {
            'limit': limit,
            'startDate': start_date,
            'filter': filter_string
        }
        response = self.get_path('/', params=params)

        return Utils.deserialize(response.text, Event)

    def get_paged_events(self, limit=None, start_date=None, after=None, filter_string=None, url=None):
        """Get a paged list of Events

        :param limit: maximum number of events to return
        :type limit: int or None
        :param filter_string: string to filter events
        :type filter_string: str or None
        :param after: event id that filtering will resume after
        :type after: str or None
        :param url: url that returns a list of Event
        :type url: str or None
        :rtype: PagedResults of Event
        """
        if url:
            response = self.get(url)

        else:
            params = {
                'limit': limit,
                'startDate': start_date,
                'after': after,
                'filter': filter_string
            }
            response = self.get_path('/', params=params)

        return PagedResults(response, Event)
