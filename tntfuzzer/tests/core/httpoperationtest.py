from unittest import TestCase, mock
from unittest.mock import patch, MagicMock

from core.httpoperation import HttpOperation
from core.replicator import Replicator
from tests.core.replicatortest import ReplicatorTest


def mock_request_get(url, params=None, headers=None, verify=False):
    pass


def mock_request_post(url, data=None, json=None, headers=None, verify=False):
    pass


def mock_request_delete(url, headers=None, verify=False):
    pass


def mock_request_put(url, data=None, headers=None, verify=False):
    pass


def random_true(obj, bit):
    return True


def random_false(obj, bit):
    return False


def create_http_op_with_random_mock(op_code, host_basepath, path, op_infos, headers, ignore_tls=True):
    replicator = Replicator(ReplicatorTest.SAMPLE_DEFINITION, True, False)
    http_op = HttpOperation(op_code, host_basepath, path,
                            op_infos, headers, replicator, False, ignore_tls)
    http_op.random.getrandbits = MagicMock(return_value=True)
    return http_op


class HttpOperationTest(TestCase):
    SAMPLE_OP_INFOS = {
        "tags": [
            "pet"
        ],
        "summary": "Updates a pet in the store with form data",
        "description": "",
        "operationId": "updatePetWithForm",
        "consumes": [
            "application/x-www-form-urlencoded"
        ],
        "produces": [
            "application/xml",
            "application/json"
        ],
        "parameters": [
            {
                "name": "petId",
                "in": "path",
                "description": "ID of pet that needs to be updated",
                "required": True,
                "type": "integer",
                "format": "int64"
            },
            {
                "name": "name",
                "in": "formData",
                "description": "Updated name of the pet",
                "required": False,
                "type": "string"
            },
            {
                "name": "status",
                "in": "formData",
                "description": "Updated status of the pet",
                "required": False,
                "type": "string"
            }
        ],
        "responses": {
            "405": {
                "description": "Invalid input"
            }
        },
        "security": [
            {
                "petstore_auth": [
                    "write:pets",
                    "read:pets"
                ]
            }
        ]
    }

    def setUp(self):
        self.http_op = create_http_op_with_random_mock('post', 'https://server.de/', 'pet/{petId}/uploadImage',
                                                       self.SAMPLE_OP_INFOS, {"X-API-Key": "abcdef123"})

    def test_replace_url_parameter_replaces_placeholder_in_url_with_type_value(self):
        url = self.http_op.replace_url_parameter(self.http_op.url, 'petId', 'integer')
        self.assertEqual(url, 'https://server.de/pet/0/uploadImage')

    def test_replace_url_parameter_replaces_only_named_param(self):
        url = self.http_op.replace_url_parameter('https://server.de/pet/{petId}/uploadImage/{imgName}',
                                                 'imgName', 'string')
        self.assertEqual(url, 'https://server.de/pet/{petId}/uploadImage/')

    def test_create_form_parameter_makes_instance_of_type_as_string(self):
        value = self.http_op.create_form_parameter('integer')
        self.assertEqual(value, '0')

    def test_is_parameter_not_optional_but_randomize_returns_true_when_param_not_optional(self):
        result = self.http_op.is_parameter_not_optional_but_randomize(parameter_required=True)
        self.assertEqual(True, result)

    def test_is_parameter_not_optional_but_randomize_returns_true_when_param_optional_and_random_true(self):
        self.http_op.random.getrandbits = MagicMock(return_value=True)
        result = self.http_op.is_parameter_not_optional_but_randomize(parameter_required=False)
        self.assertEqual(True, result)

    def test_is_parameter_not_optional_but_randomize_returns_false_when_param_optional_and_random_false(self):
        self.http_op.random.getrandbits = MagicMock(return_value=False)
        result = self.http_op.is_parameter_not_optional_but_randomize(parameter_required=False)
        self.assertEqual(False, result)

    def test_execute_with_unrecognizable_http_op_will_result_in_Nonetype_response(self):
        self.http_op = create_http_op_with_random_mock('OGRE', 'https://server.de/', 'pet/{petId}/uploadImage',
                                                       self.SAMPLE_OP_INFOS, {"X-API-Key": "abcdef123"})
        result = self.http_op.execute()
        self.assertIsNone(result)

    @patch('requests.get', side_effect=mock_request_get)
    def test_execute_with_parameter_definition_will_send_request_without_parameters_set(self, mock_get):
        definition_no_parameters = self.SAMPLE_OP_INFOS
        definition_no_parameters.pop('parameters', 0)
        self.http_op = create_http_op_with_random_mock('get', 'https://server.de/', 'pet/{petId}/uploadImage',
                                                       definition_no_parameters, {"X-API-Key": "abcdef123"})
        self.http_op.execute()
        self.assertIn(mock.call(params={}, headers={"X-API-Key": "abcdef123"},
                                url='https://server.de/pet/{petId}/uploadImage', verify=False), mock_get.call_args_list)

    @patch('requests.post', side_effect=mock_request_post)
    def test_execute_will_post__op_request_with_params_when_form_data_param_set(self, mock_post):
        self.http_op.execute()
        self.assertIn(mock.call(data={'status': '', 'name': ''}, json=None, headers={"X-API-Key": "abcdef123"},
                                url='https://server.de/pet/0/uploadImage', verify=False), mock_post.call_args_list)

    @patch('requests.get', side_effect=mock_request_get)
    def test_execute_will_get_op_request_with_url_and_params_when_form_data_param_set(self, mock_get):
        self.http_op = create_http_op_with_random_mock('get', 'https://server.de/', 'pet/{petId}/uploadImage',
                                                       self.SAMPLE_OP_INFOS, {"X-API-Key": "abcdef123"})
        self.http_op.execute()
        self.assertIn(mock.call(params={'status': '', 'name': ''},
                                url='https://server.de/pet/0/uploadImage', headers={"X-API-Key": "abcdef123"}, verify=False),
                      mock_get.call_args_list)

    @patch('requests.delete', side_effect=mock_request_delete)
    def test_execute_will_delete_op_request_with_url_only(self, mock_delete):
        self.http_op = create_http_op_with_random_mock('delete', 'https://server.de/', 'pet/{petId}/uploadImage',
                                                       self.SAMPLE_OP_INFOS, {"X-API-Key": "abcdef123"})
        self.http_op.execute()
        self.assertIn(mock.call(url='https://server.de/pet/0/uploadImage', headers={"X-API-Key": "abcdef123"}, verify=False),
                      mock_delete.call_args_list)

    @patch('requests.put', side_effect=mock_request_put)
    def test_execute_will_put_op_request_with_url_and_params_when_form_data_param_set(self, mock_put):
        self.http_op = create_http_op_with_random_mock('put', 'https://server.de/', 'pet/{petId}/uploadImage',
                                                       self.SAMPLE_OP_INFOS, {"X-API-Key": "abcdef123"})
        self.http_op.execute()
        self.assertIn(mock.call(data={'status': '', 'name': ''}, headers={"X-API-Key": "abcdef123"},
                                url='https://server.de/pet/0/uploadImage', verify=False), mock_put.call_args_list)
