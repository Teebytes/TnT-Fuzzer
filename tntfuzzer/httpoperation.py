import json
import requests

from replicator import Replicator


class HttpOperation:
    def __init__(self, op_code, host_basepath, path, op_infos):
        self.op_code = op_code
        self.url = host_basepath + path
        self.op_infos = op_infos

    def execute(self, type_definitions):
        url = self.url
        body = None
        form_data = dict()

        for parameter in self.op_infos['parameters']:
            # catch path parameters and replace them in url
            if 'path' == parameter['in']:
                url = self.replace_url_parameter(type_definitions, url, parameter['name'], parameter['type'])

            if 'body' == parameter['in']:
                body = self.create_body(type_definitions, parameter)

            if 'formData' == parameter['in']:
                form_data[parameter['name']] = self.create_form_parameter(type_definitions, parameter['type'])

        if self.op_code == 'post':
            print('post to ' + url)
            if bool(form_data):
                response = requests.post(url=url, data=form_data, json=None)
            else:
                response = requests.post(url=url, data=None, json=body)

        if self.op_code == 'get':
            print('get to ' + url)
            response = requests.get(url=url, params=form_data)

        if self.op_code == 'delete':
            print('delete to ' + url)
            response = requests.delete(url=url)

        if self.op_code == 'put':
            print('put to ' + url)
            response = requests.put(url=url, data=form_data)

        return response

    def replace_url_parameter(self, type_definitions, url, name, object_type):
        value = Replicator(type_definitions, object_type).create_init_value(object_type)
        new_url = url.replace('{' + name + '}', str(value))
        return new_url

    def create_form_parameter(self, type_definitions, object_type):
        value = Replicator(type_definitions, object_type).create_init_value(object_type)
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
            result += Replicator(type_definitions, object_type).as_json()

        return result
