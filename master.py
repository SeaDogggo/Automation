import sys
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

    target = str()
    working_dir = str()

    def __init__(self):
        self.logger = Logger('Master')
        self.recon_path = get_recon_path()
        self.recon_project_path = get_project_path()
        self.run()

    def run(self):
        self.parse_args()
        if not self.target:
            self.logger.error('Provide target with -t')
            return

        self.discover_subdomains()
        HttProbe(self.working_dir).run_all()
        # UrlScraper('{}/domains-all'.format(self.working_dir), self.working_dir).run_all()
        # Meg(self.working_dir).run()
        Subjack(self.working_dir).run()

    def parse_args(self):
        for i, arg in enumerate(sys.argv):
            if arg == '-t':
                self.set_working_dir(i)

    def set_working_dir(self, i):
        self.target = sys.argv[i + 1]
        self.working_dir = '{}/library/{}/{}'.format(self.recon_path, self.target, datetime.today().strftime('%d-%m-%Y'))
        mkdir(self.working_dir)

    def discover_subdomains(self):
        Amass(self.target, self.working_dir).run_all()
        MassDns(self.working_dir, self.recon_project_path).run_all()
        DomainCollector(self.working_dir).collect_discovered_domains()


Master()
