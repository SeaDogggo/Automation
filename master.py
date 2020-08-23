import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from amass.amass import Amass


class Master:

    target = str()
    working_dir = str()

    def __init__(self):
        self.run()

    def run(self):
        self.parse_args()
        if not self.target:
            self.log('Provide target with -t')
            return

        Amass(self.target, self.working_dir).run_all()

        # self.run_sub_domain_brute_force()
        self.remove_wildcard_sub_domains()

    def parse_args(self):
        for i, arg in enumerate(sys.argv):
            if arg == '-t':
                self.target = sys.argv[i + 1]
                self.working_dir = self.target + '/' + datetime.today().strftime('%d-%m-%Y')
                self.mkdir(self.working_dir)

    def mkdir(self, name):
        Path(name).mkdir(parents=True, exist_ok=True)

    def log(self, msg):
        print('[+] {}'.format(msg))

    def run_sub_domain_brute_force(self):
        if self.has_subdomain_bruteforce_run_today():
            self.log('Skipping domain brute force')
            return

        domain_file = Path('{}/domains'.format(self.working_dir))
        full_path = os.getcwd() + '/' + str(domain_file)

        with open('{}/domains-brute'.format(self.working_dir), "w") as outfile:
            subprocess.run(['bruteDomains', full_path], stdout=outfile)

        self.log('Domain brute force finished')

    def has_subdomain_bruteforce_run_today(self):
        domain_file = Path('{}/domains-brute'.format(self.working_dir))
        print(os.getcwd() + '/' + str(domain_file))
        return domain_file.is_file()

    def remove_wildcard_sub_domains(self):
        return True


Master()
