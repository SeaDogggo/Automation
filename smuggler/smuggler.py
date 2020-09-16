import subprocess

from command_line.util import get_smuggler_path
from file.util import does_file_exist
from file.util import mkdir
from logger.logger import Logger


class Smuggler:

    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.logger = Logger('Smuggler')
        self.results_file = '{}/smuggler/results'.format(self.working_dir)
        self.domains_probed = '{}/domains-probed'.format(working_dir)

    def run(self):
        if does_file_exist(self.results_file):
            self.logger.info('Skipping Smuggler')
            return

        self.logger.info('Started Smuggler')
        mkdir('{}/smuggler'.format(self.working_dir))
        cat = subprocess.Popen(['cat', self.domains_probed], stdout=subprocess.PIPE)
        subjack = subprocess.Popen(self.get_smuggler_cmd(), stdin=cat.stdout)
        subjack.wait()
        self.logger.info('Finished Smuggler')

    def get_smuggler_cmd(self):
        return ['python3',
                get_smuggler_path(),
                '-l',
                self.results_file,
                '-q']

