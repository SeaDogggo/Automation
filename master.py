import sys
from datetime import datetime

from amass.amass import Amass
from command_line.util import get_recon_path
from file.util import mkdir
from httprobe.httprobe import HttProbe
from logger.logger import Logger
from massdns.massdns import MassDns


class Master:

    target = str()
    working_dir = str()

    def __init__(self):
        self.logger = Logger('Master')
        self.run()

    def run(self):
        self.parse_args()
        if not self.target:
            self.logger.error('Provide target with -t')
            return

        Amass(self.target, self.working_dir).run_all()
        MassDns(self.working_dir).run_all()
        HttProbe(self.working_dir).run_all()
        # UrlScraper('{}/domains-all'.format(self.working_dir), self.working_dir).run_all()

    def parse_args(self):
        for i, arg in enumerate(sys.argv):
            if arg == '-t':
                self.set_working_dir(i)

    def set_working_dir(self, i):
        recon_path = get_recon_path()
        self.target = sys.argv[i + 1]
        self.working_dir = '{}/library/{}/{}'.format(recon_path, self.target, datetime.today().strftime('%d-%m-%Y'))
        mkdir(self.working_dir)


Master()
