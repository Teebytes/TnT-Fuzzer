from unittest import TestCase

from core.replicator import Replicator, ReplicationException


class ReplicatorTest(TestCase):
    SAMPLE_DEFINITION = {
        "Order": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "format": "int64"
                },
                "petId": {
                    "type": "integer",
                    "format": "int64"
                },
                "quantity": {
                    "type": "integer",
                    "format": "int32"
                },
                "shipDate": {
                    "type": "string",
                    "format": "date-time"
                },
                "status": {
                    "type": "string",
                    "description": "Order Status",
                    "enum": [
                        "placed",
                        "approved",
                        "delivered"
                    ]
                },
                "complete": {
                    "type": "boolean",
                    "default": False
                }
            },
            "xml": {
                "name": "Order"
            }
        },
        "Category": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "format": "int64"
                },
                "name": {
                    "type": "string"
                }
            },
            "xml": {
                "name": "Category"
            }
        },
        "User": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "format": "int64"
                },
                "username": {
                    "type": "string"
                },
                "firstName": {
                    "type": "string"
                },
                "lastName": {
                    "type": "string"
                },
                "email": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                },
                "phone": {
                    "type": "string"
                },
                "userStatus": {
                    "type": "integer",
                    "format": "int32",
                    "description": "User Status"
                }
            },
            "xml": {
                "name": "User"
            }
        },
        "Tag": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "format": "int64"
                },
                "name": {
                    "type": "string"
                }
            },
            "xml": {
                "name": "Tag"
            }
        },
        "Pet": {
            "type": "object",
            "required": [
                "name",
                "photoUrls"
            ],
            "properties": {
                "id": {
                    "type": "integer",
                    "format": "int64"
                },
                "category": {
                    "$ref": "#/definitions/Category"
                },
                "name": {
                    "type": "string",
                    "example": "doggie"
                },
                "photoUrls": {
                    "type": "array",
                    "xml": {
                        "name": "photoUrl",
                        "wrapped": True
                    },
                    "items": {
                        "type": "string"
                    }
                },
                "tags": {
                    "type": "array",
                    "xml": {
                        "name": "tag",
                        "wrapped": True
                    },
                    "items": {
                        "$ref": "#/definitions/Tag"
                    }
                },
                "status": {
                    "type": "string",
                    "description": "pet status in the store",
                    "enum": [
                        "available",
                        "pending",
                        "sold"
                    ]
                }
            },
            "xml": {
                "name": "Pet"
            }
        },
        "ApiResponse": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "integer",
                    "format": "int32"
                },
                "type": {
                    "type": "string"
                },
                "message": {
                    "type": "string"
                }
            }
        },
        "FailObject": {
            "type": "object",
            "properties": {
                "exists": {
                    "$ref": "#/definitions/ApiResponse"
                },
                "notexists": {
                    "$ref": "#/definitions/DoesNotExist"
                }
            }
        }
    }

    def setUp(self):
        self.replicator = Replicator(definitions=self.SAMPLE_DEFINITION,
                                     use_string_pattern=True,
                                     init_rand_values=False)

    def test_as_dict_creates_object_from_definition_and_has_all_fields(self):
        self.replicator = Replicator(definitions=self.SAMPLE_DEFINITION,
                                     use_string_pattern=True,
                                     init_rand_values=False)
        result = self.replicator.as_dict('#/definitions/ApiResponse')
        self.assertIsNotNone(result['code'])
        self.assertEqual(str(type(result['code'])), "<class 'int'>")
        self.assertIsNotNone(result['type'])
        self.assertEqual(str(type(result['type'])), "<class 'str'>")
        self.assertIsNotNone(result['message'])
        self.assertEqual(str(type(result['message'])), "<class 'str'>")

    def test_as_dict_creates_nested_object_from_definition_and_has_all_fields(self):
        self.replicator = Replicator(definitions=self.SAMPLE_DEFINITION,
                                     use_string_pattern=True,
                                     init_rand_values=False)
        result = self.replicator.as_dict('#/definitions/Pet')
        self.assertIsNotNone(result['id'])
        self.assertIsNotNone(result['name'])
        self.assertIsNotNone(result['photoUrls'])
        self.assertEqual(str(type(result['photoUrls'])), "<class 'list'>")

        # nested array of objects
        self.assertIsNotNone(result['tags'])
        self.assertIsNotNone(result['tags'][0]['name'])

        # nested object
        self.assertIsNotNone(result['category'])
        self.assertEqual(str(type(result['category']['id'])), "<class 'int'>")
        self.assertEqual(str(type(result['category']['name'])), "<class 'str'>")

    def test_as_dict_create_nested_object_not_in_definition_results_in_error(self):
        self.replicator = Replicator(definitions=self.SAMPLE_DEFINITION,
                                     use_string_pattern=True,
                                     init_rand_values=False)
        self.assertRaises(ReplicationException, self.replicator.as_dict, '#/definitions/FailObject')

    def test_as_json_returns_created_object_as_json(self):
        self.assertEqual(self.replicator.as_json('#/definitions/Tag'), '{"id": 0, "name": ""}')
