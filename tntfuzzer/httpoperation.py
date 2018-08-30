import json
from argparse import Namespace

import requests
from pyjfuzz.core.pjf_configuration import PJFConfiguration
from pyjfuzz.core.pjf_factory import PJFFactory

from replicator import Replicator


class HttpOperation:
    def __init__(self, op_code, host_basepath, path, op_infos, headers, use_fuzzing=True):
        self.op_code = op_code
        self.url = host_basepath + path
        self.op_infos = op_infos
        self.use_fuzzing = use_fuzzing
        self.fuzzer = None
        self.request_body = None
        self.headers = headers

    def fuzz(self, json_str):
        if self.use_fuzzing is False:
            return json_str

        if self.fuzzer is None:
            config = PJFConfiguration(Namespace(json=json.loads(json_str), nologo=True, level=6))
            self.fuzzer = PJFFactory(config)
        return self.fuzzer.fuzzed

    def execute(self, type_definitions):
        url = self.url
        form_data = dict()

        # I know this isn't much of a fuzz.. but some paths in specs have no parameters
        if 'parameters' in self.op_infos:
            for parameter in self.op_infos['parameters']:
                # catch path parameters and replace them in url
                if 'path' == parameter['in']:
                    url = self.replace_url_parameter(type_definitions, url, parameter['name'], parameter['type'])

                if 'body' == parameter['in']:
                    self.request_body = self.create_body(type_definitions, parameter)
                    self.request_body = self.fuzz(self.request_body)

                if 'formData' == parameter['in'] or 'query' == parameter['in']:
                    type_cls = parameter['type']
                    if 'array' == type_cls:
                        type_cls = parameter['items']['type']
                    form_data[parameter['name']] = self.create_form_parameter(type_definitions, type_cls)

        if self.op_code == 'post':
            if bool(form_data):
                response = requests.post(url=url, data=form_data, json=None)
            else:
                response = requests.post(url=url, data=None, json=self.request_body)

        elif self.op_code == 'get':
            response = requests.get(url=url, params=form_data)

        elif self.op_code == 'delete':
            response = requests.delete(url=url)

        elif self.op_code == 'put':
            response = requests.put(url=url, data=form_data)

        else:
            response = None

        return response

    def replace_url_parameter(self, type_definitions, url, name, object_type):
        if name is not None and object_type is not None:
            value = Replicator(type_definitions, object_type, self.use_fuzzing).create_init_value(object_type)
            new_url = url.replace('{' + name + '}', str(value))
            return new_url
        else:
            return url

    def create_form_parameter(self, type_definitions, object_type):
        value = Replicator(type_definitions, object_type, self.use_fuzzing).create_init_value(object_type)
        return str(value)

    def create_body(self, type_definitions, parameter):
        result = ''
        if 'type' in parameter['schema'] and parameter['schema']['type'] == 'array':
            object_type = parameter['schema']['items']['$ref']
            list_bodyitem = list()
            list_bodyitem.append(Replicator(type_definitions, object_type).as_dict())
            result += json.dumps(list_bodyitem)
        else:
            object_type = parameter['schema']['$ref']
            result += Replicator(type_definitions, object_type, self.use_fuzzing).as_json()

        return result
