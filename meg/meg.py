import subprocess

from file.util import mkdir
from logger.logger import Logger


class Meg:

    def __init__(self, working_dir):
        self.logger = Logger('Meg')
        self.working_dir = working_dir
        self.probed_domains = '{}/domains-probed'.format(working_dir)
        self.meg_ready_domains = '{}/meg/hosts'.format(working_dir)

    def run(self):
        mkdir('{}/meg'.format(self.working_dir))
        self.prepare_domains_for_meg()
        # self.meg_domains()

    def prepare_domains_for_meg(self):
        with open(self.meg_ready_domains, 'w') as outfile:
            awk = subprocess.Popen(['awk', '{for(i=0;i<2;i++){if(i==0)print"http://"$0; else if (i==1) print"https://"$0;}}', self.probed_domains], stdout=outfile)
            awk.wait()

    # def meg_domains(self):





