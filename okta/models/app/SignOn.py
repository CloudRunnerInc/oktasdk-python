class SignOn:

    types = {
        'loginUrl': str,
        'redirectUrl': str
    }

    def __init__(self):

        # App's login page URL
        self.loginUrl = None  # str

        # Redirect URL
        self.redirectUrl = None  # str
