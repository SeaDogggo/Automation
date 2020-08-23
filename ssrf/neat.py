import sys
import urllib.parse as urlparse
from urllib.parse import parse_qs


class NeatShit:

    NEAT_PARAMS = ['url', 'uri', 'path', 'redirect', 'url_from', 'file']
    NEAT_VALUES = ['http', 'https', '.com']
    target = ''
    quiet = False

    def __init__(self):
        self.target = sys.argv[1]
        self.set_quiet()
        self.log('[+] Looking for injectable urls, target - {}'.format(self.target))
        self.prepare_neat_params()
        self.run()
        self.log('[+] Finished')

    def log(self, msg):
        if not self.quiet:
            print(msg)

    def set_quiet(self):
        if len(sys.argv) >= 3 and sys.argv[2] == '-q':
            self.quiet = True

    def prepare_neat_params(self):
        upper_params = list()
        for param in self.NEAT_PARAMS:
            upper_params.append(param.upper())

        self.NEAT_PARAMS = self.NEAT_PARAMS + upper_params

    def run(self):
        for url in sys.stdin:
            parse_result = urlparse.urlparse(url)
            params = parse_qs(parse_result.query)
            new_url = self.inject_payload(parse_result, params)
            if not self.quiet and not new_url and self.find_potentially_neat_params(params):
                self.log('[+] Potential neatness discovered {}'.format(url))
            elif new_url:
                print('{}'.format(new_url))

    def find_neat_params(self, params):
        neat_params = list()
        for key, value in params.items():
            if key in self.NEAT_PARAMS:
                neat_params.append(key)

        return neat_params

    def inject_payload(self, parse_result, params):
        neat_params = self.find_neat_params(params)
        if len(neat_params):
            url = '{}://{}{}?{}'.format(
                parse_result.scheme,
                parse_result.netloc,
                parse_result.path,
                self.construct_query(params, neat_params)
            )
            return url

    def construct_query(self, params, neat_params):
        query = ''
        for param, values in params.items():
            if param in neat_params:
                values = [self.target]

            for value in values:
                query += '{}={}&'.format(param, value)

        return query[:-1]

    def find_potentially_neat_params(self, params):
        for param, values in params.items():
            for neat_param in self.NEAT_PARAMS:
                if neat_param in param:
                    return True
            for value in values:
                for neat_value in self.NEAT_VALUES:
                    if neat_value in value:
                        return True


NeatShit()
