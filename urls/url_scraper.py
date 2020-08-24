import os
import subprocess
import urllib.parse as urlparse
from urllib.parse import parse_qs


class UrlScraper:

    NEAT_PARAMS = ['url', 'uri', 'path', 'redirect', 'url_from', 'file', 'upload']
    NEAT_VALUES = ['http', 'https', '.com', '.net', '.org']

    def __init__(self, targets_file, working_dir):
        self.targets_file = targets_file
        self.collaborator = self.get_collaborator()
        # self.all_results = '{}/urls-all'.format(working_dir)
        self.neat_results = '{}/urls-neat'.format(working_dir)
        self.collaborator_results = '{}/urls-collaborator'.format(working_dir)

    def log(self, msg):
        print('[+] {}'.format(msg))

    def run_all(self):
        self.log('Started archived url scraping')
        if not self.collaborator:
            self.log('Collaborator env variable not set')
            return

        collaborator_file = open(self.collaborator_results, 'w')
        neat_results_file = open(self.neat_results, 'w')
        self.prepare_neat_params()

        for target in open(self.targets_file).read().split('\n'):
            all_urls = subprocess.Popen(['urls', target], stdout=subprocess.PIPE)
            for url in all_urls.stdout:
                if not url:
                    continue

                parse_result = urlparse.urlparse(url)
                params = parse_qs(parse_result.query)

                self.scrape_neat_params(collaborator_file, params, parse_result)
                self.scrape_neat_urls(neat_results_file, params, url)

            all_urls.wait()

        self.log('Finished archived url scraping')

    def get_collaborator(self):
        try:
            return os.environ['COLLABORATOR_TARGET']
        except KeyError:
            return ''

    def prepare_neat_params(self):
        upper_params = list()
        for param in self.NEAT_PARAMS:
            upper_params.append(param.upper())

        self.NEAT_PARAMS = self.NEAT_PARAMS + upper_params

    def scrape_neat_params(self, results_file, params, parse_result):
        neat_params = self.find_potentially_neat_params(params)
        if len(neat_params) > 0:
            new_url = self.inject_payload(parse_result, params, neat_params)
            results_file.write('{}\n'.format(new_url))

    def scrape_neat_urls(self, results_file, params, url):
        neat_values = self.find_potentially_neat_values(params)
        if neat_values:
            results_file.write('{}\n'.format(url))

    def inject_payload(self, parse_result, params, neat_params):
        url = '{}://{}{}?{}'.format(
            parse_result.scheme,
            parse_result.netloc,
            parse_result.path,
            self.construct_query(params, neat_params))
        return url

    def construct_query(self, params, neat_params):
        query = ''
        for param, values in params.items():
            if neat_params in param:
                values = [self.collaborator]

            for value in values:
                query += '{}={}&'.format(param, value)

        return query[:-1]

    def find_potentially_neat_params(self, params):
        results = list()
        for param, values in params.items():
            for neat_param in self.NEAT_PARAMS:
                if neat_param in param:
                    results.append(param)

        return results

    def find_potentially_neat_values(self, params):
        for _, values in params.items():
            for value in values:
                for neat_value in self.NEAT_VALUES:
                    if neat_value in value:
                        return True


# UrlScraper('/home/markus/Documents/bounty/tools/recon/shein.com/24-08-2020/domains-all', '/home/markus/Documents/bounty/tools/recon').run_all()
