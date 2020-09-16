import argparse
from datetime import datetime

from amass.amass import Amass
from command_line.util import get_recon_path, get_project_path
from file.domain_collector import DomainCollector
from file.util import mkdir
from httprobe.httprobe import HttProbe
from logger.logger import Logger
from massdns.massdns import MassDns
from subjack.subjack import Subjack


class Master:

    args = object
    targets = list()

    def __init__(self):
        self.logger = Logger('Master')
        self.recon_path = get_recon_path()
        self.recon_project_path = get_project_path()
        self.parse_args()
        self.run_all()

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--target', type=str, help='Target domain')
        parser.add_argument('--file', type=str, help='File of list of target domains')
        parser.add_argument('--massdns', action='store_true', help='Brute force subdomains using MassDns and commonspeak')
        self.args = parser.parse_args()

    def run_all(self):
        self.set_targets()
        if len(self.targets) == 0:
            self.logger.error('Targets not provided use --target or --file')

        for target in self.targets:
            self.run(target)

    def set_targets(self):
        if self.args.target:
            self.targets.append(self.args.target)
        else:
            for target in open(self.args.file).read().split('\n'):
                if target and target != '':
                    self.targets.append(target)

    def run(self, target):
        working_dir = self.create_working_dir(target)
        self.discover_subdomains(target, working_dir)
        HttProbe(working_dir).run_all()
        # UrlScraper('{}/domains-all'.format(working_dir), working_dir).run_all()
        # Meg(working_dir).run()
        Subjack(working_dir).run()

    def create_working_dir(self, target):
        working_dir = '{}/library/{}/{}'.format(self.recon_path, target, datetime.today().strftime('%d-%m-%Y'))
        mkdir(working_dir)
        return working_dir

    def discover_subdomains(self, target, working_dir):
        Amass(target, working_dir).run_all()
        if self.args.massdns:
            MassDns(working_dir, self.recon_project_path).run_all()
        DomainCollector(working_dir).collect_discovered_domains()


Master()
