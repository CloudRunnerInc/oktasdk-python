from okta.SessionsClient import SessionsClient
from okta.framework.OktaError import OktaError
import unittest
import requests_mock


@unittest.skip("Not mocked yet")
class SessionsClientTest(unittest.TestCase):
    def setUp(self):
        self.client = SessionsClient("http://okta.mock.invalid", "mock-api-key")
        self.username = "admin"
        self.password = "mock-password"

    @requests_mock.Mocker()
    def test_create_session(self, m):
        session = self.client.create_session(self.username, self.password)
        self.assertIsNotNone(session.id, "The session wasn't created with an id")

        session = self.client.create_session_with_cookie_token(self.username, self.password)
        self.assertIsNotNone(session.cookieToken, "The session wasn't created with a cookieToken")

        session = self.client.create_session_with_cookie_token_url(self.username, self.password)
        self.assertIsNotNone(session.cookieTokenUrl, "The session wasn't created with a cookieTokenUrl")

    @requests_mock.Mocker()
    def test_validate_session(self, m):
        session = self.client.create_session(self.username, self.password)

        # This shouldn't throw an error
        session = self.client.validate_session(session.id)

    @requests_mock.Mocker()
    def test_extend_session(self, m):
        session = self.client.create_session(self.username, self.password)

        # This shouldn't throw an error
        session = self.client.extend_session(session.id)

    @requests_mock.Mocker()
    def test_close_session(self, m):
        session = self.client.create_session(self.username, self.password)

        self.client.clear_session(session.id)
        self.assertRaises(OktaError, self.client.validate_session, session.id)
