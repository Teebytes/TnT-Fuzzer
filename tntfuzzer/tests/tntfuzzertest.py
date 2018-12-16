from unittest import TestCase

from tntfuzzer import TntFuzzer, SchemaException


def mock_exit(value):
    pass


def mock_get_swagger_spec(url):
    return {}


def mock_get_swagger_spec_version_1(url):
    return {'swagger': '1.0'}


def mock_get_swagger_spec_version_2(url):
    return {'swagger': '2.0', 'basePath': '', 'paths': {}, 'definitions': {}}


def mock_get_swagger_spec_version_3(url):
    return {'swagger': '3.0'}


class TntFuzzerTest(TestCase):

    def test_tntfuzzer_throws_exception_when_version_not_stated_in_schema(self):
        fuzzer = TntFuzzer('http://notexistant/swagger.json', 1, None, True, 20, True)
        fuzzer.get_swagger_spec = mock_get_swagger_spec

        self.assertRaises(SchemaException, fuzzer.start)

    def test_tntfuzzer_throws_exception_when_swagger_version_1_used(self):
        fuzzer = TntFuzzer('http://notexistant/swagger.json', 1, None, True, 20, True)
        fuzzer.get_swagger_spec = mock_get_swagger_spec_version_1

        self.assertRaises(SchemaException, fuzzer.start)

    def test_tntfuzzer_throws_exception_when_swagger_version_3_used(self):
        fuzzer = TntFuzzer('http://notexistant/swagger.json', 1, None, True, 20, True)
        fuzzer.get_swagger_spec = mock_get_swagger_spec_version_3

        self.assertRaises(SchemaException, fuzzer.start)

    def test_tntfuzzer_starts_fuzzing_when_version_2_used(self):
        fuzzer = TntFuzzer('http://notexistant/swagger.json', 1, None, True, 20, True)
        fuzzer.get_swagger_spec = mock_get_swagger_spec_version_2

        self.assertTrue(fuzzer.start())
