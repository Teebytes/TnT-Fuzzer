from unittest import TestCase

from tntfuzzer.replicator import Replicator, ReplicationException


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
        self.replicator = Replicator(definitions=self.SAMPLE_DEFINITION, object_type='#/definitions/Tag')

    def test_as_dict_creates_object_from_definition_and_has_all_fields(self):
        self.replicator = Replicator(definitions=self.SAMPLE_DEFINITION, object_type='#/definitions/ApiResponse')
        result = self.replicator.as_dict()
        self.assertIsNotNone(result['code'])
        self.assertEquals(str(type(result['code'])), "<type 'int'>")
        self.assertIsNotNone(result['type'])
        self.assertEquals(str(type(result['type'])), "<type 'str'>")
        self.assertIsNotNone(result['message'])
        self.assertEquals(str(type(result['message'])), "<type 'str'>")

    def test_as_dict_creates_nested_object_from_definition_and_has_all_fields(self):
        self.replicator = Replicator(definitions=self.SAMPLE_DEFINITION, object_type='#/definitions/Pet')
        result = self.replicator.as_dict()
        self.assertIsNotNone(result['id'])
        self.assertIsNotNone(result['name'])
        self.assertIsNotNone(result['photoUrls'])
        self.assertEquals(str(type(result['photoUrls'])), "<type 'list'>")

        # nested array of objects
        self.assertIsNotNone(result['tags'])
        self.assertIsNotNone(result['tags'][0]['name'])

        # nested object
        self.assertIsNotNone(result['category'])
        self.assertEquals(str(type(result['category']['id'])), "<type 'int'>")
        self.assertEquals(str(type(result['category']['name'])), "<type 'str'>")

    def test_as_dict_create_nested_object_not_in_definition_results_in_error(self):
        self.replicator = Replicator(definitions=self.SAMPLE_DEFINITION, object_type='#/definitions/FailObject')
        self.assertRaises(ReplicationException, self.replicator.as_dict)

    def test_as_json_returns_created_object_as_json(self):
        self.assertEquals(self.replicator.as_json(), '{"id": 0, "name": ""}')
