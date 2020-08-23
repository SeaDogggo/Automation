import subprocess
from pathlib import Path


class Amass:

    def __init__(self, target, working_dir):
        self.target = target
        self.working_dir = working_dir
        self.passive_scan_results = '{}/domains-passive'.format(self.working_dir)
        self.brute_force_results = '{}/domains-brute'.format(self.working_dir)
        self.amass_results = '{}/domains-all-amass'.format(self.working_dir)

    def run_all(self):
        self.log('Starting amass jobs')
        self.run_passive_scan(self.target)
        self.run_brute_force(self.target)
        self.aggregate_results()
        self.log('Finished amass jobs')

    def run_passive_scan(self, target):
        if self.has_amass_run_today(self.passive_scan_results):
            self.log('Skipping amass passive scan')
            return

        self.log('Amass passive scan started')
        with open(self.passive_scan_results, "w") as outfile:
            subprocess.run(['amass', 'enum', '--passive', '-d', target], stdout=outfile)
        self.log('Amass passive scan finished')

    def run_brute_force(self, target):
        if self.has_amass_run_today(self.brute_force_results):
            self.log('Skipping amass brute force')
            return

        self.log('Amass brute force started')
        with open(self.brute_force_results, "w") as outfile:
            subprocess.run(['amass', 'enum', '-brute', '-d', target], stdout=outfile)
        self.log('Amass brute force finished')

    def log(self, msg):
        print('[+] {}'.format(msg))

    def has_amass_run_today(self, scan_results):
        domain_file = Path(scan_results)
        return domain_file.is_file()

    def aggregate_results(self):
        with open(self.amass_results, "w") as outfile:
            cat = subprocess.Popen(['cat', self.passive_scan_results, self.brute_force_results], stdout=subprocess.PIPE)
            subprocess.Popen(['sort', '-u'], stdin=cat.stdout, stdout=outfile)

