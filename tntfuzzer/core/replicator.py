import json
import string
import sys
from random import Random
from randomdict import RandomDict

from core.pattern import Pattern


class ReplicationException(Exception):
    pass


class Replicator:
    """Replicates objects for requests in json format from definitions"""

    def __init__(self, definitions, use_string_pattern, init_rand_values, max_string_len=200):
        """Creates a Replicator for given type

        :parameter definitions all object definitions that could be referenced in the type that should be replicated
        :parameter use_string_pattern if valid, generated patterns instead of random character strings
        :parameter init_rand_values indicates if the replicated values should be random or - as per default - be 0 or ''
        :parameter max_string_len maximum length of strings, which are generated
        """
        self.definitions = definitions
        self.init_rand_values = init_rand_values
        self.use_string_pattern = use_string_pattern
        self.max_string_len = max_string_len
        self.random = Random()
        self.randomdict = RandomDict()

    def create_init_value(self, object_type):
        if object_type == 'integer':
            if self.init_rand_values:
                return self.random.randint(0, sys.maxsize)
            else:
                return 0
        if object_type == 'string':
            if self.init_rand_values:
                if self.use_string_pattern:
                    return Pattern.gen(self.random.randint(0, self.max_string_len))
                else:
                    return self.randomword(self.random.randint(0, self.max_string_len))
            else:
                return ''
        if object_type == 'number':
            if self.init_rand_values:
                return self.random.uniform(0, sys.maxsize)
            else:
                return 0
        if object_type == 'boolean':
            if self.init_rand_values:
                return bool(self.random.getrandbits(1))
            else:
                return False
        if object_type == 'object':
            # FIXME: get props from object and rerun with data types
            return self.randomdict.__dict__
        if object_type == 'file':
            return '/file/to/../something'  # TODO: react to init_rand_values
        return self.replicate(object_type)

    def replicate(self, object_type):
        object_class = object_type.replace('#/definitions/', '')

        if not self.definition_contains_object_class(object_class):
            raise ReplicationException('Object type "' + object_class +
                                       '" (from Swagger JSON) not found in given definitions.')

        object_schema = self.definitions[object_class]
        object_instance = {}
        for prop in object_schema['properties']:
            if 'type' in object_schema['properties'][prop]:
                prop_type = object_schema['properties'][prop]['type']
            else:
                prop_type = object_schema['properties'][prop]['$ref']

            if prop_type == 'array':
                if '$ref' in object_schema['properties'][prop]['items']:
                    array_type = object_schema['properties'][prop]['items']['$ref']
                else:
                    array_type = object_schema['properties'][prop]['items']['type']
                object_instance[prop] = list()
                object_instance[prop].append(self.create_init_value(array_type))

            else:
                object_instance[prop] = self.create_init_value(prop_type)

        return object_instance

    def definition_contains_object_class(self, object_class):
        if object_class in self.definitions:
            return True
        else:
            return False

    def randomword(self, length):
        letters = string.ascii_lowercase
        return ''.join(self.random.choice(letters) for i in range(length))

    def as_dict(self, object_type):
        return self.replicate(object_type)

    def as_json(self, object_type):
        return json.dumps(self.as_dict(object_type))
