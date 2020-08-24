import json
import subprocess

from file.util import does_file_exist
from logger.logger import Logger


class MassDns:

    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.logger = Logger('MassDns')
        self.results = '{}/domains-brute-massdns'.format(working_dir)
        self.targets_file = '{}/domains-all-amass'.format(working_dir)
        self.black_list = '{}/../config/blacklists/massdns'.format(working_dir)
        self.word_list_file = '{}/../../massdns/commonspeak'.format(working_dir)
        self.resolvers = '{}/../../massdns/resolvers.txt'.format(working_dir)

    def run_all(self):
        self.logger.info('Starting MassDNS jobs')
        if does_file_exist(self.results):
            self.logger.info('Skipping MassDNS brute force')
            return

        self.brute_force_domains()
        self.logger.info('Finished MassDNS jobs')

    def brute_force_domains(self):
        domains = open(self.targets_file).read().split('\n')
        blacklist = open(self.black_list).read().split('\n')

        for domain in domains:
            if not domain or domain in blacklist:
                continue

            sub_domains = self.construct_sub_domains(domain)
            self.get_massdns(sub_domains)

    def construct_sub_domains(self, root_domain):
        word_list = open(self.word_list_file).read().split('\n')
        sub_domains = list()

        for word in word_list:
            if not word.strip():
                continue

            sub_domains.append('{}.{}\n'.format(word.strip(), root_domain))

        return sub_domains

    def execute_and_read(self, cmd, tagets):
        domains_str = bytes('\n'.join(tagets), 'ascii')
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.PIPE)
        stdout, _ = proc.communicate(input=domains_str)
        proc.wait()
        return [j.decode('utf-8').strip() for j in stdout.splitlines() if j != b'\n']

    def get_massdns(self, targets):
        cmd = [
            'massdns',
            '-s', '10000',
            '-t', 'A',
            '-o', 'J',
            '-r', self.resolvers,
            '--flush'
        ]

        file = open(self.results, 'a')
        for line in self.execute_and_read(cmd, targets):
            if not line:
                continue

            result = json.loads(line.strip())

            try:
                answers = result['data']['answers']
                file.write('{}\n'.format(result['name'][:-1]))
            except KeyError:
                continue
