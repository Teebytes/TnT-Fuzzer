class Curlcommand:

    def __init__(self, url, method, data):
        self.url = url
        self.method = method
        self.data = data

    def get(self):
        return "curl -X" + self.method.upper() + " -H \"Content-type: application/json\" -d '" + self.data + "' " \
               + self.url
