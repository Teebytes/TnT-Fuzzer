from unittest import TestCase

from core.curlcommand import CurlCommand


class CurlCommandTest(TestCase):

    def test_get_method(self):
        method = "get"
        url = "http://example.com/api/v2/test"
        data = "{\"id\": 1, \"name\": \"Foo\"}"
        headers = u'{}'
        curlcommand = CurlCommand(url, method, data, headers)

        self.assertEquals(curlcommand.get(), "curl -XGET -H \"Content-type: application/json\" -d "
                                             "'{\"id\": 1, \"name\": \"Foo\"}' http://example.com/api/v2/test")

    def test_post_method(self):
        method = "pOsT"
        url = "http://example.com/api/post"
        data = "{\"id\": 2, \"name\": \"Bar\"}"
        headers = u'{}'
        curlcommand = CurlCommand(url, method, data, headers)

        self.assertEquals(curlcommand.get(), "curl -XPOST -H \"Content-type: application/json\" -d "
                                             "'{\"id\": 2, \"name\": \"Bar\"}' http://example.com/api/post")

    def test_empty_data(self):
        method = "get"
        url = "http://example.com/api/v2/list"
        data = ""
        headers = u'{}'
        curlcommand = CurlCommand(url, method, data, headers)
        self.assertEquals(curlcommand.get(), "curl -XGET -H \"Content-type: application/json\" "
                                             "http://example.com/api/v2/list")

    def test_generate_headers(self):
        method = "get"
        url = "http://example.com/api/v2/list"
        data = ""
        headers = '{ \"X-API-Key\": \"abcdef12345\", \"user-agent\": \"tntfuzzer\" }'
        expected_result = u'-H \"Content-type: application/json\" -H \"X-API-Key\": \"abcdef12345\" ' \
                          u'-H \"user-agent\": \"tntfuzzer\"'
        curlcommand = CurlCommand(url, method, data, headers)
        self.assertEquals(curlcommand.generate_headers(), expected_result)

    def test_generate_headers_returns_contenttype_only_when_headers_nonetype(self):
        method = "get"
        url = "http://example.com/api/v2/list"
        data = ""
        expected_result = u'-H \"Content-type: application/json\"'

        curlcommand = CurlCommand(url, method, data, None)

        self.assertEquals(curlcommand.generate_headers(), expected_result)
