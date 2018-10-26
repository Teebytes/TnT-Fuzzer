import json
import requests

from argparse import Namespace
from random import Random

from pyjfuzz.core.pjf_configuration import PJFConfiguration
from pyjfuzz.core.pjf_factory import PJFFactory


class HttpOperation:
    def __init__(self, op_code, host_basepath, path, op_infos, headers, replicator, use_fuzzing=True):
        self.op_code = op_code
        self.url = host_basepath + path
        self.op_infos = op_infos
        self.use_fuzzing = use_fuzzing
        self.replicator = replicator
        self.fuzzer = None
        self.request_body = None
        self.headers = headers
        self.random = Random()

    def fuzz(self, json_str):
        if self.use_fuzzing is False:
            return json_str

        if self.fuzzer is None:
            config = PJFConfiguration(Namespace(json=json.loads(json_str), nologo=True, level=6))
            self.fuzzer = PJFFactory(config)
        return self.fuzzer.fuzzed

    def execute(self):
        url = self.url
        form_data = dict()

        if 'parameters' in self.op_infos:
            for parameter in self.op_infos['parameters']:
                # catch path parameters and replace them in url
                if 'path' == parameter['in']:
                    url = self.replace_url_parameter(url, parameter['name'], parameter['type'])

                if 'body' == parameter['in']:
                    self.request_body = self.create_body(parameter)
                    self.request_body = self.fuzz(self.request_body)

                if 'formData' == parameter['in'] or 'query' == parameter['in']:
                    type_cls = parameter['type']
                    if 'array' == type_cls:
                        type_cls = parameter['items']['type']

                    if self.is_parameter_not_optional_but_randomize(parameter['required']):
                        form_data[parameter['name']] = self.create_form_parameter(type_cls)

        if self.op_code == 'post':
            if bool(form_data):
                response = requests.post(url=url, data=form_data, json=None, headers=self.headers)
            else:
                response = requests.post(url=url, data=None, json=self.request_body, headers=self.headers)

        elif self.op_code == 'get':
            response = requests.get(url=url, params=form_data, headers=self.headers)

        elif self.op_code == 'delete':
            response = requests.delete(url=url, headers=self.headers)

        elif self.op_code == 'put':
            response = requests.put(url=url, data=form_data, headers=self.headers)

        else:
            response = None

        return response

    def replace_url_parameter(self, url, name, object_type):
        if name is not None and object_type is not None:
            value = self.replicator.create_init_value(object_type)
            new_url = url.replace('{' + name + '}', str(value))
            return new_url
        else:
            return url

    def create_form_parameter(self, object_type):
        value = self.replicator.create_init_value(object_type)
        return str(value)

    def is_parameter_not_optional_but_randomize(self, parameter_required):
        if parameter_required:
            return True

        if bool(self.random.getrandbits(1)):
            return True

        return False

    def create_body(self, parameter):
        result = ''
        if 'type' in parameter['schema'] and parameter['schema']['type'] == 'array':
            object_type = parameter['schema']['items']['$ref']
            list_bodyitem = list()
            list_bodyitem.append(self.replicator.as_dict(object_type))
            result += json.dumps(list_bodyitem)
        else:
            object_type = parameter['schema']['$ref']
            result += self.replicator.as_json(object_type)

        return result
