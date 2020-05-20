import json
import requests

from argparse import Namespace
from random import Random

from pyjfuzz.core.pjf_configuration import PJFConfiguration
from pyjfuzz.core.pjf_factory import PJFFactory
from pyjfuzz.core.errors import PJFInvalidType


class HttpOperation:
    def __init__(self, op_code, host_basepath, path, op_infos, headers, replicator, use_fuzzing=True, ignore_tls=False):
        self.op_code = op_code
        self.url = host_basepath.rstrip("/") + "/" + path.lstrip("/")
        self.op_infos = op_infos
        self.use_fuzzing = use_fuzzing
        self.replicator = replicator
        self.fuzzer = None
        self.request_body = None
        self.headers = headers
        self.ignore_tls = ignore_tls
        self.random = Random()

    def fuzz(self, json_str):
        if self.use_fuzzing is False:
            return json_str

        if self.fuzzer is None:
            try:
                config = PJFConfiguration(Namespace(json=json.loads(json_str), nologo=True, level=6))
                self.fuzzer = PJFFactory(config)
            except PJFInvalidType:
                return json_str
        return self.fuzzer.fuzzed

    def execute(self):
        url = self.url
        form_data = dict()
        verify_tls = not self.ignore_tls  # ignore_tls defaults to False, but verify=False will disable TLS verification

        if 'parameters' in self.op_infos:
            for parameter in self.op_infos['parameters']:
                # catch path parameters and replace them in url
                if 'path' == parameter['in']:
                    if 'type' in parameter:
                        parameter_type = parameter['type']
                    elif 'type' in parameter['schema']:
                        parameter_type = parameter['schema']['type']
                    else:
                        parameter_type = parameter['schema']['$ref'].split('/')[-1]
                    url = self.replace_url_parameter(url, parameter['name'], parameter_type)

                if 'body' == parameter['in']:
                    self.request_body = self.create_body(parameter)
                    self.request_body = self.fuzz(self.request_body)

                if 'formData' == parameter['in'] or 'query' == parameter['in']:
                    if 'type' in parameter:
                        type_cls = parameter['type']
                    elif 'type' in parameter['schema']:
                        type_cls = parameter['schema']['type']
                    else:
                        type_cls = parameter['schema']['$ref'].split('/')[-1]
                    if 'array' == type_cls:
                        if 'items' in parameter and 'type' in parameter['items']:
                            type_cls = parameter['items']['type']
                        if ('schema' in parameter and 'items' in parameter['schema'] and
                           'type' in parameter['schema']['items']):
                            type_cls = parameter['schema']['items']['type']
                        else:
                            type_cls = parameter['schema']['items']['$ref'].split('/')[-1]

                    if 'required' in parameter and self.is_parameter_not_optional_but_randomize(parameter['required']):
                        form_data[parameter['name']] = self.create_form_parameter(type_cls)

        if self.op_code == 'post':
            if bool(form_data):
                response = requests.post(url=url, data=form_data, json=None, headers=self.headers, verify=verify_tls)
            else:
                response = requests.post(url=url, data=None, json=self.request_body, headers=self.headers,
                                         verify=verify_tls)

        elif self.op_code == 'get':
            response = requests.get(url=url, params=form_data, headers=self.headers, verify=verify_tls)

        elif self.op_code == 'delete':
            response = requests.delete(url=url, headers=self.headers, verify=verify_tls)

        elif self.op_code == 'put':
            response = requests.put(url=url, data=form_data, headers=self.headers, verify=verify_tls)

        elif self.op_code == 'patch':
            response = requests.patch(url=url, data=form_data, headers=self.headers, verify=verify_tls)

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
        if 'type' in parameter['schema']:
            if parameter['schema']['type'] == 'array':
                list_bodyitem = list()
                if '$ref' in parameter['schema']['items']:
                    object_type = parameter['schema']['items']['$ref']
                    list_bodyitem.append(self.replicator.as_dict(object_type))
                else:
                    object_type = parameter['schema']['items']['type']
                    list_bodyitem.append(self.replicator.create_init_value(object_type))
                result += json.dumps(list_bodyitem)
            else:
                object_type = parameter['schema']['type']
                object_value = self.replicator.create_init_value(object_type)
                if object_type == 'string':
                    object_value = '"' + object_value + '"'
                result += object_value
        else:
            object_type = parameter['schema']['$ref']
            result += self.replicator.as_json(object_type)

        return result
