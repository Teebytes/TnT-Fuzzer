import json

class CurlCommand:
    def __init__(self, url, method, data, headers):
        self.url = url
        self.method = method
        self.data = data
        self.headers = headers

    def get(self):
        if not self.data or len(self.data) < 1:
            curl_command = "curl -X" + self.method.upper() + self.generate_headers() \
                           + self.url
        else:
            curl_command = "curl -X" + self.method.upper() + self.generate_headers() + \
                                                             "-d '" + self.data + "' " + self.url

        return curl_command

    def generate_headers(self):
        headers_string = " -H \"Content-type: application/json\""
        headers = json.loads(self.headers)
        if not bool(headers):
            return headers_string
        else:
            for key, value in headers.items():
                headers_string += " -H \"" + key + "\": \"" + value + "\""
        return headers_string.strip(" ")


