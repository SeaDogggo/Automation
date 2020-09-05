import subprocess

from file.util import does_file_exist
from logger.logger import Logger


class HttProbe:

    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.logger = Logger('Httprobe')
        self.results = '{}/domains-probed'.format(working_dir)
        self.all_domains = '{}/domains-all'.format(working_dir)

    def run_all(self):
        self.logger.info('Starting httprobe jobs')
        self.run_httprobe()
        self.logger.info('Finished httprobe jobs')

    def run_httprobe(self):
        if does_file_exist(self.results):
            self.logger.info('Skipping httprobe')
            return

        self.httprobe()

    def httprobe(self):
        with open(self.results, "w") as outfile:
            cat = subprocess.Popen(['cat', self.all_domains], stdout=subprocess.PIPE)
            probe = subprocess.Popen(['httprobe'], stdin=cat.stdout, stdout=subprocess.PIPE)
            sed_0 = subprocess.Popen(['sed', 's/http:\/\///g'], stdin=probe.stdout, stdout=subprocess.PIPE)
            sed_1 = subprocess.Popen(['sed', 's/https:\/\///g'], stdin=sed_0.stdout, stdout=subprocess.PIPE)
            sort = subprocess.Popen(['sort', '-u'], stdin=sed_1.stdout, stdout=outfile)
            sort.wait()
