import argparse
import termcolor

from bravado.client import SwaggerClient

from __init__ import __version__
from httpoperation import HttpOperation
from resultvalidatior import ResultValidator


class TntFuzzer:

    def __init__(self, url, log_unexpected_errors_only):
        self.url = url
        self.log_unexpected_errors_only = log_unexpected_errors_only

    def start(self):
        print('Fetching open API from: ' + self.url)

        client = SwaggerClient.from_url(self.url)
        spec = client.swagger_spec.spec_dict

        host_basepath = spec['host'] + spec['basePath']
        paths = spec['paths']
        type_definitions = spec['definitions']
        for path_key in paths.keys():
            print('Proccessing Path: ' + path_key)

            path = paths[path_key]
            for op_code in path.keys():
                operation = HttpOperation(op_code, 'http://' + host_basepath, path_key, op_infos=path[op_code])

                response = operation.execute(type_definitions)
                validator = ResultValidator()
                log = validator.evaluate(response, path[op_code]['responses'], self.log_unexpected_errors_only)

                # log to screen for now
                print(log)


if __name__ == "__main__":
    print(termcolor.colored('___________  ___________     ___________', color='red'))
    print(termcolor.colored('\__    ___/__\__    ___/     \_   _____/_ __________________ ___________ ', color='red'))
    print(termcolor.colored('  |    | /    \|    |  ______ |    __)|  |  \___   /\___   // __ \_  __ \\', color='red'))
    print(termcolor.colored('  |    ||   |  \    | /_____/ |     \ |  |  //    /  /    /\  ___/|  | \/', color='red'))
    print(termcolor.colored('  |____||___|  /____|         \___  / |____//_____ \/_____ \\\\___  >__|   ', color='red'))
    print(termcolor.colored('    Dynamite ', 'green') + termcolor.colored('\/', 'red') +
          termcolor.colored(' for your API!', 'green') +
          termcolor.colored('     \/              \/      \/    \/    ', 'red') +
          termcolor.colored('   v', 'green') + termcolor.colored(__version__, 'blue'))
    print('')

    parser = argparse.ArgumentParser()

    parser.add_argument('--url', metavar='<URL>', type=str,
                        help='The URL pointing to your OpenAPI implementation e.g. '
                             'http://petstore.swagger.io/v2/swagger.json')

    parser.add_argument('--log_all', action='store_true',
                        help='If set, all responses are logged. The expected responses and the '
                             'unexpected ones. Per default only unexpected responses are logged.')

    args = vars(parser.parse_args())

    if args['url'] is None:
        parser.print_usage()
    else:
        tnt = TntFuzzer(url=args['url'], log_unexpected_errors_only=not args['log_all'])
        tnt.start()
