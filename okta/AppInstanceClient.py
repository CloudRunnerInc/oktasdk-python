from okta.models.app.AppUser import AppUser
from okta.framework.ApiClient import ApiClient
from okta.framework.Utils import Utils
from okta.framework.PagedResults import PagedResults
from okta.models.app.AppInstance import AppInstance


class AppInstanceClient(ApiClient):
    def __init__(self, base_url, api_token):
        ApiClient.__init__(self, base_url + '/api/v1/apps', api_token)

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
        response = ApiClient.get_path(self, '/', params=params)
        return Utils.deserialize(response.text, AppInstance)

    def get_paged_app_instances(self, limit=None, filter_string=None, after=None, url=None):
        """Get a paged list of AppInstances

        :param limit: maximum number of apps to return
        :type limit: int or None
        :param filter_string: string to filter apps
        :type filter_string: str or None
        :param after: app id that filtering will resume after
        :type after: str
        :param url: url that returns a list of AppInstance
        :type url: str
        :rtype: PagedResults of AppInstance
        """
        if url:
            response = ApiClient.get(self, url)

        else:
            params = {
                'limit': limit,
                'after': after,
                'filter': filter_string
            }
            response = ApiClient.get_path(self, '/', params=params)

        return PagedResults(response, AppInstance)

    def create_app_instance(self, app_instance):
        """Create a app instance

        :param app_instance: the data to create a user
        :type app_instance: AppInstance
        :rtype: AppInstance
        """
        response = ApiClient.post_path(self, '/', app_instance)
        return Utils.deserialize(response.text, AppInstance)

    def get_app_instance(self, id):
        """Get a single app

        :param id: the app id
        :type id: str
        :rtype: AppInstance
        """
        response = ApiClient.get_path(self, '/{0}'.format(id))
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
        response = ApiClient.put_path(self, '/{0}'.format(id), app_instance)
        return Utils.deserialize(response.text, AppInstance)

    def delete_app_instance(self, id):
        """Delete app by target id

        :param id: the target app id
        :type id: str
        :return: None
        """
        ApiClient.delete_path(self, '/{0}'.format(id))

    # LIFECYCLE

    def activate_app_instance(self, id):
        """Activate app by target id

        :param id: the target app id
        :type id: str
        :return: None
        """
        ApiClient.post_path(self, '/{0}/lifecycle/activate'.format(id), None)

    def deactivate_app_instance(self, id):
        """Deactivate app by target id

        :param id: the target app id
        :type id: str
        :return: None
        """
        ApiClient.post_path(self, '/{0}/lifecycle/deactivate'.format(id), None)

    # USER

    def get_assigned_user_by_id_to_app(self, aid, uid):
        """Get the assigned user to an application by user id

        :param aid: the target app id
        :type aid: str
        :param uid: the target user id
        :type uid: str
        :rtype: AppUser
        """
        response = ApiClient.get_path(self, '/{0}/users/{1}'.format(aid, uid))
        return Utils.deserialize(response.text, AppUser)

    def get_assigned_user_to_app(self, aid, user):
        """Get the assigned user to an application

        :param aid: the target app id
        :type aid: str
        :param user: the target User
        :type user: User
        :rtype: AppUser
        """
        return self.get_assigned_user_to_app(aid, user.id)

    def get_assigned_users_to_app(self, aid):
        """Get assigned users to an application

        :param aid: the target app id
        :type aid: str
        :rtype: Array of AppUser
        """
        response = ApiClient.get_path(self, '/{0}/users'.format(aid))
        return Utils.deserialize(response.text, AppUser)

    def assign_user_to_app_for_SSO(self, aid, user):
        """Assigns a user to an application for SSO

        :param aid: the target app id
        :type aid: str
        :param user: the target User
        :type user: User
        :rtype: AppUser
        """
        return self.assign_user_by_id_to_app_for_SSO(aid, user.id)

    def assign_user_by_id_to_app_for_SSO(self, aid, uid):
        """Assigns a user to an application for SSO

        :param aid: the target app id
        :type aid: str
        :param uid: the target user id
        :type uid: str
        :rtype: AppUser
        """
        params = {
            'id': uid,
        }
        response = ApiClient.post_path(self, '/{0}/users'.format(aid), params)
        return Utils.deserialize(response.text, AppUser)