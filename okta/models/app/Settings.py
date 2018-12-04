from okta.models.app.AppSettings import AppSettings
from okta.models.app.SignOn import SignOn


class Settings:

    types = {
        'app': AppSettings,
        'signOn': SignOn
    }

    def __init__(self):

        self.app = None  # AppSettings

        self.signOn = None  # SignOn
