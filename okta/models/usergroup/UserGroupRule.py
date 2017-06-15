class UserGroupRule:

    types = {
        'type': str,
        'id': str,
        'name': str,
        'conditions': dict,
        'expressions': dict,
        'actions': dict,
    }

    def __init__(self):

        # type of the group rule
        self.type = None  # str

        # id of the group rule
        self.id = None  # str

        # name of the group rule
        self.name = None  # str

        # name of the group rule
        self.conditions = None  # GroupRuleConditions

        # name of the group rule
        self.actions = None  # GroupRuleActions
