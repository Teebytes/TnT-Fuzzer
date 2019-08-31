import argparse
import json
import requests
import termcolor
import urllib3
import sys

from core.curlcommand import CurlCommand
from core.httpoperation import HttpOperation
from core.resultvalidatior import ResultValidator
from core.replicator import Replicator
from utils.strutils import StrUtils
from urllib.parse import urlparse

version = "2.3.0"


class SchemaException(Exception):
    pass


class TntFuzzer:

    def __init__(self, url, iterations, headers, log_unexpected_errors_only, 
                    max_string_length, use_string_pattern, ignore_tls=False, host=None, basepath=None):
        self.url = url
        self.iterations = iterations
        self.headers = headers
        self.log_unexpected_errors_only = log_unexpected_errors_only
        self.max_string_length = max_string_length
        self.use_string_pattern = use_string_pattern
        self.ignore_tls = ignore_tls        
        self.host = host
        self.basepath = basepath

        if self.ignore_tls:
            # removes warnings for insecure connections
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def start(self):
        print('Fetching open API from: ' + self.url)

        # Try to find the protocol, host and basePath from the Swagger spec.
        # host and schemes can be omitted, and the "standard" says you should use the spec's URL to derive them.
        # https://swagger.io/docs/specification/2-0/api-host-and-base-path/
        schemes = []
        host = None
        basePath = None

        try:
            spec = self.get_swagger_spec(self.url)
            specURL = urlparse(self.url)
        except json.JSONDecodeError:
            error_cant_connect()

        if 'swagger' not in spec:
            self.log_operation(None, self.url,
                               {
                                   "status_code": "000",
                                   "documented_reason": "Specification: no version string found",
                                   "body": "Specification: no version string found in Swagger spec"
                               }, '')
            raise SchemaException

        if not spec['swagger'].startswith('2'):
            self.log_operation(None, self.url,
                               {
                                   "status_code": "000",
                                   "documented_reason": "Specification: wrong specification version",
                                   "body": "Specification: version in swagger spec not supported"
                               }, '')
            raise SchemaException

        if 'schemes' in spec:
            schemes = spec['schemes']
        else:
            # fake the array we'd find in the spec
            schemes.append(specURL.scheme)
            self.log_operation(None, self.url,
                               {
                                   "status_code": "000",
                                   "documented_reason": "Specification: no schemes entry, fallback to spec URL scheme",
                                   "body": "Specification: host entry not present in Swagger spec"}, '')

        if self.host:
            host = self.host
        elif 'host' in spec:
            host = spec['host']
        else:
            host = specURL.netloc
            self.log_operation(None, self.url,
                               {
                                   "status_code": "000",
                                   "documented_reason": "Specification: no host entry, fallback to spec URL host",
                                   "body": "Specification: schemes entry not present in Swagger spec"
                               }, '')

        # There is no nice way to derive the basePath from the spec's URL. They *have* to include it
        if 'basePath' not in spec:
            self.log_operation(None, self.url,
                               {
                                   "status_code": "000",
                                   "documented_reason": "Specification: basePath entry missing from Swagger spec",
                                   "body": "Specification Error: basePath entry missing from Swagger spec"
                               }, '')
            raise SchemaException
        basePath = self.basepath if self.basepath else spec['basePath']
        host_basepath = host + basePath

        paths = spec['paths']
        type_definitions = spec['definitions']
        # the specifcation can list multiple schemes (http, https, ws, wss) - all should be tested.
        # Each scheme is a potentially different end point
        replicator = Replicator(type_definitions, self.use_string_pattern, True, self.max_string_length)
        for protocol in schemes:
            for path_key in paths.keys():
                path = paths[path_key]

                for op_code in path.keys():
                    operation = HttpOperation(op_code, protocol + '://' + host_basepath, path_key,
                                              replicator=replicator, op_infos=path[op_code], use_fuzzing=True,
                                              headers=self.headers, ignore_tls=self.ignore_tls)

                    for _ in range(self.iterations):
                        response = operation.execute()
                        validator = ResultValidator()
                        log = validator.evaluate(response, path[op_code]['responses'], self.log_unexpected_errors_only)
                        curlcommand = CurlCommand(response.url, operation.op_code, operation.request_body, self.headers, self.ignore_tls)

                        # log to screen for now
                        self.log_operation(operation.op_code, response.url, log, curlcommand)

        return True

    def log_operation(self, op_code, url, log, curlcommand):
        status_code = str(log['status_code'])
        documented_reason = log['documented_reason']
        body = log['body'].replace('\n', ' ')

        if documented_reason is None:
            StrUtils.print_log_row(op_code, url, status_code, 'None', body, curlcommand)
        else:
            if not self.log_unexpected_errors_only:
                StrUtils.print_log_row(op_code, url, status_code, documented_reason, body, curlcommand)

    def get_swagger_spec(self, url):
        verify_tls = not self.ignore_tls # ignore_tls defaults to False, but verify=False will disable TLS verification
        return json.loads(requests.get(url=url, headers=self.headers, verify=verify_tls).text)


def error_cant_connect():
    print('Unable to get swagger file :-(')
    sys.exit(1)


def main():
    print(termcolor.colored(r'___________  ___________     ___________', color='red'))
    print(termcolor.colored(r'\__    ___/__\__    ___/     \_   _____/_ __________________ ___________ ', color='red'))
    print(termcolor.colored(r'  |    | /    \|    |  ______ |    __)|  |  \___   /\___   // __ \_  __ \\', color='red'))
    print(termcolor.colored(r'  |    ||   |  \    | /_____/ |     \ |  |  //    /  /    /\  ___/|  | \/', color='red'))
    print(termcolor.colored(r'  |____||___|  /____|         \___  / |____//_____ \/_____ \\\\___  >__|   ', color='red'))
    print(termcolor.colored(r'    Dynamite ', 'green') + termcolor.colored(r'\/', 'red') +
          termcolor.colored(r' for your API!', 'green') +
          termcolor.colored(r'     \/              \/      \/    \/    ', 'red') +
          termcolor.colored(r'   v', 'green') + termcolor.colored(version, 'blue'))
    print('')

    parser = argparse.ArgumentParser()

    parser.add_argument('--url', type=str,
                        help='The URL pointing to your OpenAPI implementation e.g. '
                             'http://petstore.swagger.io/v2/swagger.json')

    parser.add_argument('--iterations', type=int, default=1,
                        help='The number of iterations one API call is fuzzed.')

    parser.add_argument('--log_all', action='store_true',
                        help='If set, all responses are logged. The expected responses and the '
                             'unexpected ones. Per default only unexpected responses are logged.')

    parser.add_argument('--headers', type=json.loads,
                        help='Send custom http headers for Cookies or api keys e.g. { \"X-API-Key\": \"abcdef12345\", '
                             '\"user-agent\": \"tntfuzzer\" }')

    parser.add_argument('--string-patterns', dest='string-patterns', action='store_true',
                        help='Use pattern generation, when string types are replicated for requests. The pattern '
                             'has a fixed reproducable form. With the search tool the position of a pattern subset'
                             'recalculated. Useful for finding positions of bufferoverflows.')

    parser.add_argument('--max-random-string-len', dest='max-random-string-len', type=int, default=200,
                        help='The maximum length of generated strings.')
    
    parser.add_argument('--ignore-cert-errors', dest='ignore-tls', action='store_true', default=False,
                        help='Ignore TLS errors, like self-signed certificates.')

    parser.add_argument('--host', type=str,
                        help='Overrides the API host specified within the swagger file.')

    parser.add_argument('--basepath', type=str,
                        help='Overrides the API basePath specified within the swagger file.')

    args = vars(parser.parse_args())

    if args['url'] is None:
        parser.print_usage()
    else:
        tnt = TntFuzzer(url=args['url'], iterations=args['iterations'], headers=args['headers'],
                        log_unexpected_errors_only=not args['log_all'], use_string_pattern=args['string-patterns'],
                        max_string_length=args['max-random-string-len'], ignore_tls=args["ignore-tls"], 
                        host=args["host"], basepath=args["basepath"])
        try:
            tnt.start()
        except SchemaException:
            print('Error: Severe schema validation error. Please look in logs for more detailed error message.')


if __name__ == "__main__":
    main()
