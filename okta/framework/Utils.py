import json
import dateutil.parser
from datetime import datetime
import types
import six
from okta.models.event.Target import Target, UserTarget, ClientTarget


class Utils(object):
    @staticmethod
    def deserialize(from_data, to_class):

        def custom_setattr(o, a, v):
            if hasattr(o, 'alt_names') and a in o.alt_names:
                a = o.alt_names[a]

            setattr(o, a, v)

        json_dump = {}
        if from_data is None or len(from_data) == 0:
            json_dump = {}
        elif isinstance(from_data, six.text_type) or isinstance(from_data, six.string_types):
            json_dump = json.loads(from_data)
        else:
            json_dump = from_data

        list_type = types.ListType if six.PY2 else list
        if isinstance(json_dump, list_type):
            obj_list = list()
            for obj in json_dump:
                obj_list.append(Utils.deserialize(obj, to_class))

            return obj_list

        else:
            obj = to_class()

            # Loop through each type of object in types
            if hasattr(to_class, 'types'):
                if getattr(to_class, 'allow_extra_fields', False):
                    for key, value in six.iteritems(json_dump):
                        if key in to_class.types:
                            continue
                        custom_setattr(obj, key, json_dump[key])
                for attr, attr_type in six.iteritems(to_class.types):
                    if attr in json_dump:
                        val = json_dump[attr]

                        if not val:
                            continue

                        if attr_type == datetime:
                            val = dateutil.parser.parse(val)

                        elif attr_type == str or attr_type == int or attr_type == dict or attr_type == bool:
                            pass

                        elif attr_type == Target:
                            for target in val:
                                if target['objectType'] == 'User':
                                    attr_type = UserTarget
                                elif target['objectType'] == 'Client':
                                    attr_type = ClientTarget

                        else:
                            val = Utils.deserialize(val, attr_type)

                        custom_setattr(obj, attr, val)

            # Otherwise, assume all the properties are strings
            else:
                for key, value in six.iteritems(json_dump):
                    custom_setattr(obj, key, json_dump[key])

            # Some models have dicts as values
            if hasattr(to_class, 'dict_types'):
                for attr, attr_type in six.iteritems(to_class.dict_types):
                    if attr in json_dump:
                        dictionary = json_dump[attr]
                        new_dict = dict()

                        for key, value in six.iteritems(dictionary):
                            val = Utils.deserialize(value, attr_type)
                            new_dict[key] = val

                        custom_setattr(obj, attr, new_dict)

            return obj

    @staticmethod
    def remove_nulls(d):
        built = {}
        for k, v in six.iteritems(d):
            if v is None:
                continue

            if isinstance(v, dict):
                built[k] = Utils.remove_nulls(v)

            if isinstance(v, object) and hasattr(v, '__dict__'):
                built[k] = Utils.remove_nulls(v.__dict__)

            else:
                built[k] = v

        return built
