from okta.AppInstanceClient import AppInstanceClient
from okta.framework.OktaError import OktaError
import unittest
from okta.models.app.AppInstance import AppInstance
import requests_mock


class SessionsClientTest(unittest.TestCase):
    def setUp(self):
        self.client = AppInstanceClient("http://okta.mock.invalid", "mock-api-key")
        self.username = "admin"
        self.password = "mock-password"

    @unittest.skip("Not mocked yet")
    @requests_mock.Mocker()
    def test_create_app(self, m):
        app = AppInstance.build_bookmark("https://www.google.com")
        app = self.client.create_app_instance(app)
        self.assertIsNotNone(app.id)

    @unittest.skip("Not mocked yet")
    @requests_mock.Mocker()
    def test_delete_app(self, m):
        app = AppInstance.build_bookmark("https://www.google.com")
        app = self.client.create_app_instance(app)
        self.client.deactivate_app_instance(app.id)
        self.client.delete_app_instance(app.id)
        self.assertRaises(OktaError, self.client.get_app_instance, app.id)
