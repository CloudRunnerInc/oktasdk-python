from okta.framework.ApiClient import ApiClient
from okta.framework.Utils import Utils
from okta.models.schema.UserSchema import UserSchema
from okta.models.schema.AppUserSchema import AppUserSchema


class SchemaClient(ApiClient):

    def __init__(self, base_url, api_token, **kwargs):
        super(SchemaClient, self).__init__(
            base_url + '/api/v1/meta/schemas',
            api_token,
            **kwargs
        )

    # CRUD

    def add_property_to_user_schema(self, user_custom_schema):
        """Adds a custom properties to the user profile.

        :param user_custom_schema: the custom property to add
        :type user_custom_schema: UserProfileCustomSubschema
        :rtype: UserSchema
        """
        response = self.post_path('/user/default',
                                  user_custom_schema)
        return Utils.deserialize(response.text, UserSchema)

    def add_property_to_app_user_schema(self, aid, app_user_custom_schema):
        """Adds a custom user profile properties to the app user schema.

        :param aid: the target app id
        :type aid: str
        :param app_user_custom_schema: the custom property to add
        :type app_user_custom_schema: AppUserProfileCustomSubschema
        :rtype: AppUserSchema
        """
        response = self.post_path('/apps/{0}/default'.format(aid),
                                  app_user_custom_schema)
        return Utils.deserialize(response.text, AppUserSchema)
