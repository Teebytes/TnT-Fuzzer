import json


class CurlCommand:

    def __init__(self, url, method, data, headers, ignore_tls=False):
        self.url = url
        self.method = method
        self.data = data
        self.headers = headers

        if ignore_tls:
            self.ignore_tls = "-k " # short for --insecure
        else:
            self.ignore_tls = ""

    def get(self):
        if not self.data or len(self.data) < 1:
            curl_command = "curl " + self.ignore_tls + "-X" + self.method.upper() + " " + self.generate_headers() \
                           + " " + self.url
        else:
            curl_command = "curl " + self.ignore_tls + "-X" + self.method.upper() + " " + \
                           self.generate_headers() + " -d '" + self.data + "' " + self.url

        return curl_command

    def generate_headers(self):
        headers_string = " -H \"Content-type: application/json\""

        if self.headers is not None:
            # self.headers is always a dict, because argparse has type=json.loads
            headers_string += " "
            for key, value in self.headers.items():
                headers_string += "-H \"" + key + "\": \"" + value + "\""
                headers_string += " "
        return headers_string.strip()
