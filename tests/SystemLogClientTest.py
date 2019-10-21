import unittest
import uuid

import requests_mock

from okta import SystemLogClient

try:
    import unittest.mock as mock
except ImportError:
    import mock


class UsersClientTest(unittest.TestCase):
    def setUp(self):
        self.client = SystemLogClient("http://okta.mock.invalid", "mock-api-key")

    @requests_mock.Mocker()
    def test_get_single_page(self, m):
        next_url = "http://okta.mock.invalid/api/v1/logs/?limit=3&after=token_1"
        m.register_uri("GET", "http://okta.mock.invalid/api/v1/logs/?limit=3", json=[
            {"version": "0", "uuid": "fbd0f023-a24e-477f-bc66-1e270d2bf561", "eventType": "mock.event"},
            {"version": "0", "uuid": "93992eb6-e5aa-4ef3-b3a9-2a44923a8c25", "eventType": "mock.event"},
            {"version": "0", "uuid": "e845dc12-1ae6-496a-b3eb-59b3919e57fd", "eventType": "mock.event"},
        ], headers={
            "Link": '<{url}>; rel="next"'.format(url=next_url)
        })

        page = self.client.get_paged_log_events(limit=3)
        result = page.result

        self.assertEqual(next_url, page.next_url)

        self.assertEqual(3, len(result))
        self.assertEqual("fbd0f023-a24e-477f-bc66-1e270d2bf561", result[0]["uuid"])

    @requests_mock.Mocker()
    def test_get_next_page(self, m):
        url = "http://okta.mock.invalid/api/v1/logs/?limit=3&after=token_1"
        next_url = "http://okta.mock.invalid/api/v1/logs/?limit=3&after=token_2"
        m.register_uri("GET", url, json=[
            {"version": "0", "uuid": "fbd0f023-a24e-477f-bc66-1e270d2bf561", "eventType": "mock.event"},
            {"version": "0", "uuid": "93992eb6-e5aa-4ef3-b3a9-2a44923a8c25", "eventType": "mock.event"},
            {"version": "0", "uuid": "e845dc12-1ae6-496a-b3eb-59b3919e57fd", "eventType": "mock.event"},
        ], headers={
            "Link": '<{url}>; rel="next"'.format(url=next_url)
        })

        page = self.client.get_next_page(url)
        result = page.result

        self.assertEqual(next_url, page.next_url)
        self.assertEqual(3, len(result))
        self.assertEqual("fbd0f023-a24e-477f-bc66-1e270d2bf561", result[0]["uuid"])

    @requests_mock.Mocker()
    def test_multiple_pages(self, m):
        all_urls = [
            "http://okta.mock.invalid/api/v1/logs/?limit=3",
            "http://okta.mock.invalid/api/v1/logs/?limit=3&after=token_1",
            "http://okta.mock.invalid/api/v1/logs/?limit=3&after=token_2",
            "http://okta.mock.invalid/api/v1/logs/?limit=3&after=token_3",
        ]
        all_items = [
            [
                {
                    "version": "0",
                    "uuid": str(uuid.uuid4()),
                    "eventType": "mock.event",
                    "displayMessage": "Event {}".format(page_idx * 3 + item_idx)
                }
                for item_idx in range(0, 3)
            ] for page_idx in range(0, 3)
        ]
        for page_idx in range(0, 3):
            url = all_urls[page_idx]
            items = all_items[page_idx]
            m.register_uri("GET", url, json=items, headers={
                "Link": '<{url}>; rel="next"'.format(url=all_urls[page_idx+1])
            })
        m.register_uri("GET", all_urls[3], json=[], headers={
            "Link": '<{url}>; rel="next"'.format(url=all_urls[3])
        })

        pages = list(self.client.get_all_log_event_pages(limit=3))
        self.assertEqual(3, len(pages))

        for page_idx, page in enumerate(pages):
            self.assertEqual(all_items[page_idx], page)

    @requests_mock.Mocker()
    @mock.patch("time.sleep")
    def test_get_all_log_events(self, m, mock_sleep):
        all_urls = [
            "http://okta.mock.invalid/api/v1/logs/?limit=3",
            "http://okta.mock.invalid/api/v1/logs/?limit=3&after=token_1",
            "http://okta.mock.invalid/api/v1/logs/?limit=3&after=token_2",
            "http://okta.mock.invalid/api/v1/logs/?limit=3&after=token_3",
        ]
        all_items = [
            [
                {
                    "version": "0",
                    "uuid": str(uuid.uuid4()),
                    "eventType": "mock.event",
                    "displayMessage": "Event {}".format(page_idx * 3 + item_idx)
                }
                for item_idx in range(0, 3)
            ] for page_idx in range(0, 3)
        ]
        for page_idx in range(0, 3):
            url = all_urls[page_idx]
            items = all_items[page_idx]
            m.register_uri("GET", url, json=items, headers={
                "Link": '<{url}>; rel="next"'.format(url=all_urls[page_idx + 1])
            })
        m.register_uri("GET", all_urls[3], json=[], headers={
            "Link": '<{url}>; rel="next"'.format(url=all_urls[3])
        })

        items_iterable = self.client.get_all_log_events(
            max_results=5,
            per_page=3,
            sleep_between_pages=1.0,
        )
        items_count = 0
        for item_idx, item in enumerate(items_iterable):
            self.assertEqual(all_items[item_idx // 3][item_idx % 3], item)
            items_count += 1
            if items_count == 4:  # After the first page, when we've got the 4th item.
                mock_sleep.assert_called_once_with(1.0)
            else:
                mock_sleep.assert_not_called()
            mock_sleep.reset_mock()
        self.assertEqual(5, items_count)
