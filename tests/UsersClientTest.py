from okta import UsersClient
from okta.models.user import User
import random
import unittest
import requests_mock


class UsersClientTest(unittest.TestCase):
    def setUp(self):
        self.client = UsersClient("http://okta.mock.invalid", "mock-api-key")

    @requests_mock.Mocker()
    def test_paging(self, m):
        m.register_uri("GET", "http://okta.mock.invalid/api/v1/users/?limit=1", json=[
            {"id": "u0001mock", "status": "ACTIVE"},
        ], headers={
            "Link": '<http://okta.mock.invalid/api/v1/users/?limit=1&offset=1>; rel="next"'
        })
        m.register_uri("GET", "http://okta.mock.invalid/api/v1/users/?limit=1&offset=1", json=[
            {"id": "u0002mock", "status": "ACTIVE"},
        ])

        users = self.client.get_paged_users(limit=1)

        first_page_hit = subsequent_page_hit = False

        for user in users.result:
            first_page_hit = True

        while not users.is_last_page():
            users = self.client.get_paged_users(url=users.next_url)
            for user in users.result:
                subsequent_page_hit = True

        self.assertTrue(first_page_hit and subsequent_page_hit, "The first and subsequent pages weren't hit")

    @requests_mock.Mocker()
    def test_single_user(self, m):
        m.register_uri(
            "POST", "http://okta.mock.invalid/api/v1/users/?activate=false",
            complete_qs=True,
            json={
                "id": "u0001mock",
                "status": "STAGED",
            },
        )
        user = User(login='fake' + str(random.random()) + '@asdf.com',
                    email='fake@asdf.com',
                    firstName='Joe',
                    lastName='Schmoe')
        user = self.client.create_user(user, activate=False)
        self.assertEqual(user.status, "STAGED", "User should be staged")

        m.register_uri(
            "POST", "http://okta.mock.invalid/api/v1/users/?activate=true",
            complete_qs=True,
            json={
                "id": "u0002mock",
                "status": "PROVISIONED",
            },
        )
        user = User(login='fake' + str(random.random()) + '@asdf.com',
                    email='fake@asdf.com',
                    firstName='Joe',
                    lastName='Schmoe')
        user = self.client.create_user(user, activate=True)
        self.assertEqual(user.status, "PROVISIONED", "User should be provisioned")
