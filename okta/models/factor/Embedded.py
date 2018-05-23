from okta.models.Link import Link


class Embedded:

    types = {
        'timeStep': int,
        'sharedSecret': str,
        'encoding': str,
        'keyLength': int,
    }

    dict_types = {
        '_links': Link
    }

    alt_names = {
        '_links': 'links'
    }

    def __init__(self):

        self.timeStep = None  # int

        self.sharedSecret = None  # str

        self.encoding = None  # str

        self.keyLength = None  # int

        self.links = None  # str
