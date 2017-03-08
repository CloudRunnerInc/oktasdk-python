from okta.framework.ApiClient import ApiClient
from okta.framework.Utils import Utils
from okta.framework.PagedResults import PagedResults
from okta.models.app.AppInstance import AppInstance
from okta.models.role.Role import Role
from okta.models.usergroup.UserGroup import UserGroup


class AdminRolesClient(ApiClient):
    def __init__(self, base_url, api_token):
        ApiClient.__init__(self, base_url + '/api/v1/users/', api_token)

    # Assignment Operations

    def get_user_admin_roles(self, user):
        """Get roles for a single user

        :param user: the user
        :type user: User
        :rtype: Array of Role
        """
        return self.get_user_admin_roles_by_id(user.id)

    def get_user_admin_roles_by_id(self, uid):
        """Get roles for a single user

        :param uid: the user id
        :type uid: str
        :rtype: Array of Role
        """
        response = ApiClient.get_path(self, '/{0}/roles'.format(uid))
        return Utils.deserialize(response.text, Role)

    def assign_admin_role_to_user_by_id(self, uid, rid):
        """Assign an admin role for a single user

        :param uid: the user id
        :type uid: str
        :param rid: the role id to be assigned to user
        :type rid: str
        :rtype: Role
        """
        response = ApiClient.post_path(self, '/{0}/roles'.format(uid), rid)
        return Utils.deserialize(response.text, Role)

    def unassign_admin_role_to_user_by_id(self, uid, rid):
        """Unassign an admin role for a single user

        :param uid: the user id
        :type uid: str
        :param rid: the role id to be unassigned to user
        :type rid: str
        :rtype: None
        """
        ApiClient.delete_path(self, '/{0}/roles/{1}'.format(uid, rid))

    # Target Operations

    # Group targets

    def get_group_targets_for_user(self, user, rid, limit=None):
        """List all groups targets for a USER_ADMIN role assignment

        :param user: the user
        :type user: User
        :param rid: the USER_ADMIN role id
        :type rid: str
        :rtype: Array of UserGroup
        """
        return self.get_group_targets_for_user_by_id(user.id, rid, limit)

    def get_group_targets_for_user_by_id(self, uid, rid, limit=None):
        """List all groups targets for a USER_ADMIN role assignment

        :param uid: the user id
        :type uid: str
        :param rid: the USER_ADMIN role id
        :type rid: str
        :param limit: maximum number of Groups to return
        :type limit: int or None
        :rtype: Array of UserGroup
        """
        params = {
            'limit': limit
        }
        url = '/{0}/roles/{1}/targets/groups'.format(uid, rid)
        response = ApiClient.get_path(self, url, params=params)
        return PagedResults(response, UserGroup)

    def add_group_target_to_user_admin(self, user, rid, gid):
        """Add a group target for a USER_ADMIN role assignment

        :param user: the user
        :type user: User
        :param rid: the USER_ADMIN role id
        :type rid: str
        :param gid: the group id to be added
        :type gid: str
        :rtype: None
        """
        return self.add_group_target_to_user_admin_by_id(user.id, rid, gid)

    def add_group_target_to_user_admin_by_id(self, uid, rid, gid):
        """Add a group target for a USER_ADMIN role assignment

        :param uid: the user id
        :type uid: str
        :param rid: the USER_ADMIN role id
        :type rid: str
        :param gid: the group id to be added
        :type gid: str
        :rtype: None
        """
        url = '/{0}/roles/{1}/targets/groups/{2}'.format(uid, rid, gid)
        ApiClient.put_path(self, url)

    # App targets

    def get_app_targets_for_user(self, user, rid, limit=None):
        """List all groups targets for a USER_ADMIN role assignment

        :param user: the user
        :type user: User
        :param rid: the APP_ADMIN role id
        :type rid: str
        :rtype: Array of Catalog Apps
        """
        return self.get_app_targets_for_user_by_id(user.id, rid, limit)

    def get_app_targets_for_user_by_id(self, uid, rid, limit=None):
        """List all groups targets for a APP_ADMIN role assignment

        :param uid: the user id
        :type uid: str
        :param rid: the APP_ADMIN role id
        :type rid: str
        :param limit: maximum number of Apps to return
        :type limit: int or None
        :rtype: Array of Catalog Apps
        """
        params = {
            'limit': limit
        }
        url = '/{0}/roles/{1}/targets/catalog/apps'.format(uid, rid)
        response = ApiClient.get_path(self, url, params=params)
        # TODO: create Catalog App Model
        return PagedResults(response, AppInstance)

    def add_app_target_to_user_admin(self, user, rid, appname):
        """Add a app target for a APP_ADMIN role assignment

        :param user: the user
        :type user: User
        :param rid: the APP_ADMIN role id
        :type rid: str
        :param appname: the name of the app to be added
        :type appname: str
        :rtype: None
        """
        return self.add_app_target_to_user_admin_by_id(user.id, rid, appname)

    def add_app_target_to_user_admin_by_id(self, uid, rid, appname):
        """Add a app target for a APP_ADMIN role assignment

        :param uid: the user id
        :type uid: str
        :param rid: the APP_ADMIN role id
        :type rid: str
        :param appname: the name of the app to be added
        :type appname: str
        :rtype: None
        """
        url = '/{0}/roles/{1}/targets/catalog/apps/{2}'.format(uid, rid, appname)
        ApiClient.put_path(self, url)

    def delete_app_target_to_user_admin(self, user, rid, appname):
        """Delete an app target for a APP_ADMIN role assignment

        :param user: the user
        :type user: User
        :param rid: the APP_ADMIN role id
        :type rid: str
        :param appname: the name of the app to be added
        :type appname: str
        :rtype: None
        """
        return self.delete_app_target_to_user_admin_by_id(user.id, rid, appname)

    def delete_app_target_to_user_admin_by_id(self, uid, rid, appname):
        """Delete an app target for a APP_ADMIN role assignment

        :param uid: the user id
        :type uid: str
        :param rid: the APP_ADMIN role id
        :type rid: str
        :param appname: the name of the app to be added
        :type appname: str
        :rtype: None
        """
        url = '/{0}/roles/{1}/targets/catalog/apps/{2}'.format(uid, rid, appname)
        ApiClient.delete_path(self, url)

