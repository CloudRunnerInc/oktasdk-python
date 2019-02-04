from okta import UserGroupsClient
from okta.models.usergroup import UserGroup
from okta import UsersClient
from okta.models.user import User
import random
import unittest
import requests_mock


class UserGroupsClientTest(unittest.TestCase):
    def setUp(self):
        self.client = UserGroupsClient("http://okta.mock.invalid", "mock-api-key")
        self.user_client = UsersClient("http://okta.mock.invalid", "mock-api-key")

    @requests_mock.Mocker()
    def test_single_group(self, m):
        name = 'random_group_' + str(random.random())
        m.register_uri("POST", "http://okta.mock.invalid/api/v1/groups/", json={
            "id": "g0001mock",
            "profile": {
                "name": name,
                "description": "something interesting here"
            },
        })
        group = UserGroup(name=name, description="something interesting here")
        group = self.client.create_group(group)
        self.assertEqual(group.profile.name, name, "The name for the group wasn't set properly")

    @requests_mock.Mocker()
    def test_add_user_to_group(self, m):
        # Create group
        m.register_uri("POST", "http://okta.mock.invalid/api/v1/groups/", json={"id": "g0001mock"})
        name = 'random_group_' + str(random.random())
        group = UserGroup(name=name, description='something interesting here')
        group = self.client.create_group(group)

        # Create user
        m.register_uri(
            "POST", "http://okta.mock.invalid/api/v1/users/?activate=false",
            json={
                "id": "u0001mock",
                "status": "STAGED",
            },
        )
        user = User(login='fake' + str(random.random()) + '@asdf.com',
                    email='fake@asdf.com',
                    firstName='Joe',
                    lastName='Schmoe')
        user = self.user_client.create_user(user, activate=False)

        m.register_uri("PUT", "http://okta.mock.invalid/api/v1/groups/g0001mock/users/u0001mock", json={})
        self.client.add_user_to_group(group, user)
