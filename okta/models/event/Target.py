from copy import copy


class Target:

    types = {
        'id': str,
        'displayName': str,
        'objectType': str
    }

    def __init__(self):

        # Unique key for actor
        self.id = None  # str

        # Name of actor used for display purposes
        self.displayName = None  # str

        # User, Client, or AppInstance
        self.objectType = None  # str


class UserTarget(Target):

    types = copy(Target.types)
    types.update({
        'login': str
    })

    def __init__(self):
        # Username
        self.login = None  # str


class ClientTarget(Target, object):

    types = copy(Target.types)
    types.update({
        'ipAddress': str
    })

    def __init__(self):
        # Client's IP Address
        self.ipAddress = None  # str