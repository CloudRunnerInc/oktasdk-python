from okta.models.app.AppUser import AppUser
from okta.framework.ApiClient import ApiClient
from okta.framework.Utils import Utils
from okta.framework.PagedResults import PagedResults
from okta.models.app.AppInstance import AppInstance


class AppInstanceClient(ApiClient):
    def __init__(self, base_url, api_token, **kwargs):
        super(AppInstanceClient, self).__init__(
            base_url + '/api/v1/apps',
            api_token,
            **kwargs
        )

    # CRUD

    def get_app_instances(self, limit=None, filter_string=None):
        """Get a list of AppInstances

        :param limit: maximum number of apps to return
        :type limit: int or None
        :param filter_string: string to filter users
        :type filter_string: str or None
        :rtype: list of AppInstance
        """
        params = {
            'limit': limit,
            'filter': filter_string
        }
        response = self.get_path('/', params=params)
        return Utils.deserialize(response.text, AppInstance)

    def get_paged_app_instances(self, limit=None, filter_string=None,
                                after=None, expand=None, url=None):
        """Get a paged list of AppInstances

        :param limit: maximum number of apps to return
        :type limit: int or None
        :param filter_string: string to filter apps
        :type filter_string: str or None
        :param after: app id that filtering will resume after
        :type after: str
        :param expand: whether to traverses users link relationship and
                       optionally embeds Application User resource
        :type: expand: bool
        :param url: url that returns a list of AppInstance
        :type url: str
        :rtype: PagedResults of AppInstance
        """
        if url:
            response = self.get(url)

        else:
            params = {
                'limit': limit,
                'after': after,
                'filter': filter_string,
                'expand': expand
            }
            response = self.get_path('/', params=params)

        return PagedResults(response, AppInstance)

    def create_app_instance(self, app_instance):
        """Create a app instance

        :param app_instance: the data to create a user
        :type app_instance: AppInstance
        :rtype: AppInstance
        """
        response = self.post_path('/', app_instance)
        return Utils.deserialize(response.text, AppInstance)

    def get_app_instance(self, id):
        """Get a single app

        :param id: the app id
        :type id: str
        :rtype: AppInstance
        """
        response = self.get_path('/{0}'.format(id))
        return Utils.deserialize(response.text, AppInstance)

    def update_app_instance(self, app_instance):
        """Update an app

        :param app_instance: the app to update
        :type app_instance: AppInstance
        :rtype: AppInstance
        """
        return self.update_app_instance_by_id(app_instance.id, app_instance)

    def update_app_instance_by_id(self, id, app_instance):
        """Update an app, defined by an id

        :param id: the target app id
        :type id: str
        :param app_instance: the data to update the target app
        :type app_instance: AppInstance
        :rtype: AppInstance
        """
        response = self.put_path('/{0}'.format(id), app_instance)
        return Utils.deserialize(response.text, AppInstance)

    def delete_app_instance(self, id):
        """Delete app by target id

        :param id: the target app id
        :type id: str
        :return: None
        """
        self.delete_path('/{0}'.format(id))

    # LIFECYCLE

    def activate_app_instance(self, id):
        """Activate app by target id

        :param id: the target app id
        :type id: str
        :return: None
        """
        self.post_path('/{0}/lifecycle/activate'.format(id), None)

    def deactivate_app_instance(self, id):
        """Deactivate app by target id

        :param id: the target app id
        :type id: str
        :return: None
        """
        self.post_path('/{0}/lifecycle/deactivate'.format(id), None)

    # USER

    def get_assigned_user_by_id_to_app(self, aid, uid):
        """Get the assigned user to an application by user id

        :param aid: the target app id
        :type aid: str
        :param uid: the target user id
        :type uid: str
        :rtype: AppUser
        """
        response = self.get_path('/{0}/users/{1}'.format(aid, uid))
        return Utils.deserialize(response.text, AppUser)

    def update_app_credentials_for_user(
            self, aid, uid, username=None, password=None):
        """Update user app credentials

        :param aid: the target app id
        :type aid: str
        :param uid: the target user id
        :type uid: str
        :param username: the target user username
        :type username: str
        :param password: the target user password
        :type password: str
        """
        params = {
            'credentials': {}
        }
        if username:
            params['credentials']['userName'] = username
        if password:
            params['credentials']['password'] = {'value': password}

        self.post_path('/{0}/users/{1}'.format(aid, uid), params)

    def update_user_app_profile(self, aid, uid, app_user_data):
        """Update app profile for assigned user (User Application Profile)

        :param aid: the target app id
        :type aid: str
        :param uid: the target user id
        :type uid: str
        :param app_user_data: profile data for the app user
        """
        params = {'profile': app_user_data}
        response = self.post_path('/{0}/users/{1}'.format(aid, uid), params)
        return Utils.deserialize(response.text, AppUser)

    def get_assigned_user_to_app(self, aid, user):
        """Get the assigned user to an application

        :param aid: the target app id
        :type aid: str
        :param user: the target User
        :type user: User
        :rtype: AppUser
        """
        return self.get_assigned_user_by_id_to_app(aid, user.id)

    def get_assigned_users_to_app(
            self, aid, limit=None, after=None, filter_string=None, url=None):
        """Get assigned users to an application
        :param aid: the target app id
        :type aid: str
        :param limit: maximum number of apps to return
        :type limit: int or None
        :param filter_string: string to filter apps
        :type filter_string: str or None
        :param after: app id that filtering will resume after
        :type after: str
        :param url: url that returns a list of AppInstance
        :type url: str
        :rtype: PagedResults of User models
        """
        if url:
            response = self.get(url)
        else:
            params = {
                'limit': limit,
                'after': after,
                'filter': filter_string
            }
            response = self.get_path('/{0}/users'.format(aid), params=params)
        return PagedResults(response, AppUser)

    def assign_user_to_app_for_SSO(self, aid, user, app_user_data={}):
        """Assigns a user to an application for SSO

        :param aid: the target app id
        :type aid: str
        :param user: the target User
        :type user: User
        :param app_user_data: additional profile data for the app user
        :type app_user_data: dict
        :rtype: AppUser
        """
        return self.assign_user_by_id_to_app_for_SSO(
            aid, user.id, app_user_data)

    def assign_user_by_id_to_app_for_SSO(self, aid, uid, app_user_data={}):
        """Assigns a user to an application for SSO

        :param aid: the target app id
        :type aid: str
        :param uid: the target user id
        :type uid: str
        :param app_user_data: additional profile data for the app user
        :type app_user_data: dict
        :rtype: AppUser
        """
        params = {
            'id': uid,
            'profile': app_user_data
        }
        response = self.post_path('/{0}/users'.format(aid), params)
        return Utils.deserialize(response.text, AppUser)

    def unassign_user_by_id_from_app(self, aid, uid):
        """Unassigns a user from an application

        :param aid: the target app id
        :type aid: str
        :param uid: the target user id
        :type uid: str
        :rtype: None
        """
        response = self.delete_path('/{0}/users/{1}'.format(
            aid, uid))
        return response.text

    def assign_group_to_app(self, aid, gid):
        """Assigns a group to an application

        :param aid: the target app id
        :type aid: str
        :param gid: the target group id
        :type gid: str
        :rtype: JSON response
        """
        response = self.put_path('/{0}/groups/{1}'.format(aid, gid))
        return response.text
