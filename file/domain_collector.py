import subprocess

from file.util import does_file_exist
from logger.logger import Logger


class DomainCollector:

    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.logger = Logger('Collector')
        self.all_domains = '{}/domains-all'.format(working_dir)
        self.blacklist_file = '{}/../config/blacklists/httprobe'.format(working_dir)

    def collect_discovered_domains(self):
        if does_file_exist(self.all_domains):
            self.logger.info('Skipped domains-all file generation')
            return

        self.logger.info('Started collecting and sorting discovered domains')
        targets = self.get_domains_files()
        self.collect_and_sort(targets)
        self.logger.info('Finished collecting and sorting discovered domains')

    def collect_and_sort(self, files):
        with open(self.all_domains, "w") as outfile:
            cat = subprocess.Popen(['awk', '1'] + files, stdout=subprocess.PIPE)

            if does_file_exist(self.blacklist_file):
                grep_blacklist = subprocess.Popen(['grep', '-v', '-f', self.blacklist_file], stdin=cat.stdout, stdout=subprocess.PIPE)
                sort = subprocess.Popen(['sort', '-u'], stdin=grep_blacklist.stdout, stdout=outfile)
                sort.wait()
            else:
                sort = subprocess.Popen(['sort', '-u'], stdin=cat.stdout, stdout=outfile)
                sort.wait()

    def get_domains_files(self):
        files = [
            '{}/amass/domains-all-amass'.format(self.working_dir),
            '{}/domains-brute-massdns'.format(self.working_dir)
        ]
        return [file for file in files if does_file_exist(file)]
