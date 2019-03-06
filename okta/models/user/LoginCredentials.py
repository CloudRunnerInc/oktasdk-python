from okta.models.user.Provider import Provider
from okta.models.user.Password import Password
from okta.models.user.RecoveryQuestion import RecoveryQuestion


class LoginCredentials:

    types = {
        'userName': str,
        'password': Password,
        'recovery_question': RecoveryQuestion,
        'provider': Provider
    }

    def __init__(self):

        self.userName = None  # str

        self.password = None  # Password

        self.recovery_question = None  # RecoveryQuestion

        self.provider = None  # Provider
