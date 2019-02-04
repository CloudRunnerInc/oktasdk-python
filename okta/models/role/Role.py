from datetime import datetime

from okta.models.Link import Link
from okta.models.Embedded import Embedded


class Role:
    types = {
        'id': str,
        'label': str,
        'type': str,
        'status': str,
        'created': datetime,
        'lastUpdated': datetime,
    }

    dict_types = {
        '_links': Link,
        '_embedded': Embedded
    }

    alt_names = {
        '_links': 'links',
        '_embedded': 'embedded'
    }

    def __init__(self):

        # unique key for user
        self.id = None  # str

        # display name of role
        self.label = None  # str

        # type of role
        self.type = None  # str

        # status of role assignment
        self.status = None  # str

        # timestamp when role was created
        self.created = None  # datetime

        # timestamp when role was last updated
        self.lastUpdated = None  # datetime
