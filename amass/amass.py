import subprocess

from file.util import does_file_exist
from file.util import mkdir
from logger.logger import Logger


class Amass:

    def __init__(self, target, working_dir):
        self.target = target
        self.logger = Logger('Amass')
        self.working_dir = working_dir
        self.passive_scan_results = '{}/amass/domains-passive'.format(self.working_dir)
        self.brute_force_results = '{}/amass/domains-brute'.format(self.working_dir)
        self.amass_results = '{}/amass/domains-all-amass'.format(self.working_dir)

    def run_all(self):
        mkdir('{}/amass'.format(self.working_dir))
        self.logger.info('Started Amass jobs')
        self.run_passive_scan(self.target)
        self.run_brute_force(self.target)
        self.aggregate_results()
        self.logger.info('Finished Amass jobs')

    def run_passive_scan(self, target):
        if does_file_exist(self.passive_scan_results):
            self.logger.info('Skipped Amass passive scan')
            return

        self.logger.info('Amass passive scan started')
        with open(self.passive_scan_results, 'w') as outfile:
            subprocess.run(['amass', 'enum', '--passive', '-d', target], stdout=outfile)
        self.logger.info('Amass passive scan finished')

    def run_brute_force(self, target):
        if does_file_exist(self.brute_force_results):
            self.logger.info('Skipped Amass brute force')
            return

        self.logger.info('Amass brute force started')
        with open(self.brute_force_results, 'w') as outfile:
            subprocess.run(['amass', 'enum', '-brute', '-d', target], stdout=outfile)
        self.logger.info('Amass brute force finished')

    def aggregate_results(self):
        with open(self.amass_results, 'w') as outfile:
            cat = subprocess.Popen(['cat', self.passive_scan_results, self.brute_force_results], stdout=subprocess.PIPE)
            sort = subprocess.Popen(['sort', '-u'], stdin=cat.stdout, stdout=outfile)
            sort.wait()

