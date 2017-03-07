from okta.framework.ApiClient import ApiClient
from okta.framework.Utils import Utils
from okta.models.role.Role import Role


class AdminRolesClient(ApiClient):
    def __init__(self, base_url, api_token):
        ApiClient.__init__(self, base_url + '/api/v1/users/', api_token)

    def get_user_admin_roles(self, user):
        """Get roles for a single user

        :param user: the user
        :type user: User
        :rtype: Array of Role
        """
        return self.get_user_admin_roles_by_id(user.id)

    def get_user_admin_roles_by_id(self, uid):
        """Get roles for a single user, defined by an id

        :param uid: the user id
        :type uid: str
        :rtype: Array of Role
        """
        response = ApiClient.get_path(self, '/{0}/roles'.format(uid))
        return Utils.deserialize(response.text, Role)
