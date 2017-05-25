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

    def get_user_admin_roles(self, uid):
        """Get roles for a single user

        :param uid: the user id
        :type uid: str
        :rtype: Array of Role
        """
        response = ApiClient.get_path(self, '/{0}/roles'.format(uid))
        return Utils.deserialize(response.text, Role)

    def assign_admin_role_to_user(self, uid, role):
        """Assign an admin role for a single user

        :param uid: the user id
        :type uid: str
        :param role: the role to be assigned to user
        :type role: str
        :rtype: Role
        """
        data = {
            'type': role
        }

        url_path = '/{0}/roles'.format(uid)
        response = ApiClient.post_path(self, url_path, data=data)
        return Utils.deserialize(response.text, Role)

    def unassign_admin_role_to_user(self, uid, rid):
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

    def get_paged_group_targets_for_user_admin(self, uid, rid, url=None, limit=None):
        """Get a paged list of group targets for an USER_ADMIN role assignment

        :param uid: the user id
        :type uid: str
        :param rid: the USER_ADMIN role id
        :type rid: str
        :param url: url that returns a list of group targets
        :type url: str
        :param limit: maximum number of Group to return
        :type limit: int or None
        :rtype: Array of UserGroup
        """
        if url:
            response = ApiClient.get(self, url)

        else:
            params = {
                'limit': limit
            }
            url_path = '/{0}/roles/{1}/targets/groups'.format(uid, rid)
            response = ApiClient.get_path(self, url_path, params=params)

        return PagedResults(response, UserGroup)

    def get_group_targets_for_user_admin(self, uid, rid, limit=None):
        """Get a list of group targets for an USER_ADMIN role assignment

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
        return Utils.deserialize(response.text, UserGroup)

    def add_group_target_to_user_admin(self, uid, rid, gid):
        """Add a group target for an USER_ADMIN role assignment

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

    def get_paged_app_targets_for_app_admin(self, uid, rid, url=None, limit=None):
        """Get a paged list of app targets for an APP_ADMIN role assignment

        :param uid: the user id
        :type uid: str
        :param rid: the APP_ADMIN role id
        :type rid: str
        :param url: url that returns a list of app targets
        :type url: str
        :param limit: maximum number of Apps to return
        :type limit: int or None
        :rtype: Array of CatalogApp
        """
        if url:
            response = ApiClient.get(self, url)

        else:
            params = {
                'limit': limit
            }
            url_path = '/{0}/roles/{1}/targets/catalog/apps'.format(uid, rid)
            response = ApiClient.get_path(self, url_path, params=params)
        # TODO: create Catalog App Model
        return PagedResults(response, AppInstance)

    def get_app_targets_for_app_admin(self, uid, rid, limit=None):
        """Get a list of app targets for an APP_ADMIN role assignment

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
        return Utils.deserialize(response.text, AppInstance)

    def add_app_target_to_app_admin(self, uid, rid, appname):
        """Add an app target for an APP_ADMIN role assignment

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

    def delete_app_target_to_app_admin(self, uid, rid, appname):
        """Delete an app target for an APP_ADMIN role assignment

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

