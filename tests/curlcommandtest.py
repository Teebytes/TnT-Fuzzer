from unittest import TestCase
from tntfuzzer.curlcommand import CurlCommand


class CurlCommandTest(TestCase):

    def test_get_method(self):
        method = "get"
        url = "http://example.com/api/v2/test"
        data = "{\"id\": 1, \"name\": \"Foo\"}"

        curlcommand = CurlCommand(url, method, data)

        self.assertEquals(curlcommand.get(), "curl -XGET -H \"Content-type: application/json\" -d "
                                             "'{\"id\": 1, \"name\": \"Foo\"}' http://example.com/api/v2/test")

    def test_post_method(self):
        method = "pOsT"
        url = "http://example.com/api/post"
        data = "{\"id\": 2, \"name\": \"Bar\"}"

        curlcommand = CurlCommand(url, method, data)

        self.assertEquals(curlcommand.get(), "curl -XPOST -H \"Content-type: application/json\" -d "
                                             "'{\"id\": 2, \"name\": \"Bar\"}' http://example.com/api/post")