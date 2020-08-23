import json
import subprocess
from pathlib import Path


class MassDns:

    def __init__(self, targets, working_dir):
        self.targets_file = targets
        self.working_dir = working_dir
        self.black_list = './massdns/blacklist'
        self.resolvers = './massdns/resolvers.txt'
        self.word_list_file = './massdns/commonspeak'
        self.results = '{}/domains-brute-massdns'.format(self.working_dir)

    def run_all(self):
        self.log('Starting MassDNS jobs')
        if self.has_massdns_run_today(self.results):
            self.log('Skipping MassDNS brute force')
            return

        self.brute_force_domains()
        self.log('Finished MassDNS jobs')

    def brute_force_domains(self):
        domains = open(self.targets_file).read().split('\n')
        blacklist = open(self.black_list).read().split('\n')

        for domain in domains:
            if not domain or domain in blacklist:
                continue

            sub_domains = self.construct_sub_domains(domain)
            self.get_massdns(sub_domains)

    def has_massdns_run_today(self, scan_results):
        domain_file = Path(scan_results)
        return domain_file.is_file()

    def log(self, msg):
        print('[+] {}'.format(msg))

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
