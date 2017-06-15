from okta.framework.ApiClient import ApiClient
from okta.framework.Utils import Utils
from okta.framework.PagedResults import PagedResults

from okta.models.usergroup.UserGroup import UserGroup
from okta.models.usergroup.UserGroupRule import UserGroupRule
from okta.models.user.User import User


class UserGroupsClient(ApiClient):
    def __init__(self, base_url, api_token):
        ApiClient.__init__(self, base_url + '/api/v1/groups', api_token)

    # CRUD

    def get_groups(self, limit=None, filter_string=None, query=None):
        """Get a list of UserGroups

        :param limit: maximum number of groups to return
        :type limit: int or None
        :param filter_string: Filter expression for groups
        :type filter_string: str or None
        :param query: string to search group names
        :type query: str or None
        :rtype: list of UserGroup
        """
        params = {
            'limit': limit,
            'filter': filter_string,
            'q': query
        }
        response = ApiClient.get_path(self, '/', params=params)
        return Utils.deserialize(response.text, UserGroup)

    def get_paged_groups(self, limit=None, filter_string=None, after=None, url=None):
        """Get a paged list of UserGroups

        :param limit: maximum number of groups to return
        :type limit: int or None
        :param filter_string: Filter expression for groups
        :type filter_string: str or None
        :param after: group id that filtering will resume after
        :type after: str
        :param url: url that returns a list of UserGroup
        :type url: str
        :rtype: PagedResults of UserGroup
        """
        if url:
            response = ApiClient.get(self, url)

        else:
            params = {
                'limit': limit,
                'filter': filter_string,
                'after': after
            }
            response = ApiClient.get_path(self, '/', params=params)

        return PagedResults(response, UserGroup)

    def get_group(self, gid):
        """Get a single group

        :param gid: the group id
        :type gid: str
        :rtype: UserGroup
        """
        response = ApiClient.get_path(self, '/{0}'.format(gid))
        return Utils.deserialize(response.text, UserGroup)

    def update_group(self, group):
        """Update a group

        :param group: the group to update
        :type group: UserGroup
        :rtype: UserGroup
        """
        return self.update_group_by_id(group.id, group)

    def update_group_by_id(self, gid, group):
        """Update a group, defined by an id

        :param gid: the target group id
        :type gid: str
        :param group: the data to update the target group
        :type group: UserGroup
        :rtype: UserGroup
        """
        response = ApiClient.put_path(self, '/{0}'.format(gid), group)
        return Utils.deserialize(response.text, UserGroup)

    def create_group(self, group=None, name=None, description=None):
        """Create a group

        :param group: the data to create a group
        :type group: UserGroup
        :param name: Name of the group to be created
        :type name: str
        :param description: Description of the group to be created
        :type description: str
        :rtype: UserGroup
        """
        if group:
            data = group
        else:
            data = UserGroup()
            data.profile = {
                    "name": name,
                    "description": description
            }

        response = ApiClient.post_path(self, '/', data)
        return Utils.deserialize(response.text, UserGroup)

    def delete_group(self, gid):
        """Delete group by target id

        :param gid: the target group id
        :type gid: str
        :return: None
        """
        response = ApiClient.delete_path(self, '/{0}'.format(gid))
        return Utils.deserialize(response.text, UserGroup)

    def add_user_to_group(self, group, user):
        """Add a user to a group

        :param group: the target group
        :type group: UserGroup
        :param user: the target user
        :type user: User
        :return: None
        """
        return self.add_user_to_group_by_id(group.id, user.id)

    def add_user_to_group_by_id(self, gid, uid):
        """Add a user to a group

        :param gid: the target group id
        :type gid: str
        :param uid: the target user id
        :type uid: str
        :return: None
        """
        response = ApiClient.put_path(self, '/{0}/users/{1}'.format(gid, uid))

    def get_group_members(self, gid, limit=None, after=None):
        """Get a list of users from a group

        :param gid: the group id
        :type gid: str
        :param limit: maximum number of users to return
        :type limit: int or None
        :param after: user id that filtering will resume after
        :type after: str
        :rtype: list of User
        """
        params = {
            'limit': limit,
            'after': after
        }
        response = ApiClient.get_path(self, '/{0}/users'.format(gid), params=params)
        return Utils.deserialize(response.text, User)

    def get_paged_group_members(self, gid, url=None, limit=None, after=None):
        """Get a paged list of users from a group

        :param gid: the group id
        :type gid: str
        :param limit: maximum number of users to return
        :type limit: int or None
        :param after: user id that filtering will resume after
        :type after: str
        :param url: url that returns a list of User
        :type url: str
        :rtype: PagedResults of User
        """
        if url:
            response = ApiClient.get(self, url)

        else:
            params = {
                'limit': limit,
                'after': after
            }
            response = ApiClient.get_path(self, '/{0}/users'.format(gid), params=params)
        return PagedResults(response, User)

    # Group Rules
    def create_group_rule(self, name=None, expression=None, groupid=None, rule=None):
        """Creates a group rule to dynamically add users to the specified
            group if they match the condition

        :param name: Name of group rule
        :type name: str
        :param expression: Expression to be used by group rule
        :type name: str
        :param groupid: Group ID of the group to assign the group rule
        :type groupid: str
        :param rule: UserGroupRule to be created
        :type rule: UserGroupRule
        :rtype: UserGroupRule
        """
        if rule:
            data = rule
        else:
            data = UserGroupRule()
            data.type = "group_rule"
            data.name = name
            data.conditions = {
                'expression': {
                    'value': expression,
                    'type': "urn:okta:expression:1.0",
                }
            }

            data.actions = {
                'assignUserToGroups': {
                    'groupIds': [groupid],
                }
            }

        response = ApiClient.post_path(self, '/rules', data=data)
        return Utils.deserialize(response.text, UserGroupRule)

    def activate_group_rule(self, rid):
        """Activates a specific group rule by id from your organization

        :param rid: Id of the rule to be activated
        :type rid: str
        :return: None
        """
        return ApiClient.post_path(self, '/rules/{0}/lifecycle/activate'.format(rid))

    def deactivate_group_rule(self, rid):
        """Deactivates a specific group rule by id from your organization

        :param rid: Id of the rule to be deactivated
        :type rid: str
        :return: None
        """
        return ApiClient.post_path(self, '/rules/{0}/lifecycle/deactivate'.format(rid))

    def delete_group_rule(self, rid):
        """Removes a specific group rule by id from your organization

        :param rid: Id of the rule to be deleted
        :type rid: str
        :return: None
        """
        return ApiClient.delete_path(self, '/rules/{0}'.format(rid))

