from okta.AuthClient import AuthClient
import unittest
import requests_mock


class SessionsClientTest(unittest.TestCase):
    def setUp(self):
        self.client = AuthClient("http://okta.mock.invalid", "mock-api-key")
        self.username = "admin"
        self.password = "mock-password"

    @requests_mock.Mocker()
    def test_simple_auth(self, m):
        m.request(
            "POST", "http://okta.mock.invalid/api/v1/authn/",
            json={"sessionToken": "mock-token"},
        )
        response = self.client.authenticate(self.username, self.password)
        self.assertTrue(response.sessionToken or response.status == 'MFA_REQUIRED', "The simple auth failed")
        self.assertEqual(1, len(m.request_history))
        data = m.last_request.json()
        self.assertEqual(self.username, data.get("username"))
        self.assertEqual(self.password, data.get("password"))
