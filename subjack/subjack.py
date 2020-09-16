import subprocess

from file.util import does_file_exist
from file.util import mkdir
from logger.logger import Logger


class Subjack:

    def __init__(self, working_dir):
        self.logger = Logger('Subjack')
        self.working_dir = working_dir
        self.results_file = '{}/subjack/results.txt'.format(self.working_dir)

    def run(self):
        if does_file_exist(self.results_file):
            self.logger.info('Skipping subjack')
            return

        self.logger.info('Started subjack')
        mkdir('{}/subjack'.format(self.working_dir))
        subjack = subprocess.Popen(self.get_subjack_cmd())
        subjack.wait()
        self.logger.info('Finished subjack')

    def get_subjack_cmd(self):
        return ['subjack',
                '-w',
                '{}/domains-all'.format(self.working_dir),
                '-t',
                '100',
                '-timeout',
                '30',
                '-o',
                self.results_file,
                '-ssl']
