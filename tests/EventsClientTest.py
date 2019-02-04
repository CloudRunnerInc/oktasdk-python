from okta.EventsClient import EventsClient
import unittest
import requests_mock


class SessionsClientTest(unittest.TestCase):
    def setUp(self):
        self.client = EventsClient("http://okta.mock.invalid", "mock-api-key")
        self.username = "admin"
        self.password = "mock-password"

    @unittest.skip("Not mocked yet")
    @requests_mock.Mocker()
    def test_get_events(self, m):
        events = self.client.get_events(limit=1)
        self.assertEqual(len(events), 1, "Limits aren't enforced on events")

        events = self.client.get_events()
        self.assertGreaterEqual(len(events), 1, "There were no events returned, when there should be")
