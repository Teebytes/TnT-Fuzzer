class CurlCommand:
    def __init__(self, url, method, data):
        self.url = url
        self.method = method
        self.data = data

    def get(self):
        if not self.data or len(self.data) < 1:
            curl_command = "curl -X" + self.method.upper() + " -H \"Content-type: application/json\" " \
                           + self.url
        else:
            curl_command = "curl -X" + self.method.upper() + " -H \"Content-type: application/json\" " \
                                                             "-d '" + self.data + "' " + self.url

        return curl_command
