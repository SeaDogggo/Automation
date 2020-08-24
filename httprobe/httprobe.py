import subprocess
from pathlib import Path


class HttProbe:

    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.results = '{}/domains-probed'.format(working_dir)
        self.all_domains = '{}/domains-all'.format(working_dir)
        self.blacklist_file = './httprobe/blacklist'

    def run_all(self):
        self.log('Starting httprobe jobs')
        self.run_httprobe()
        self.log('Finished httprobe jobs')

    def log(self, msg):
        print('[+] {}'.format(msg))

    def run_httprobe(self):
        if self.does_file_exist(self.results):
            self.log('Skipping httprobe')
            return

        self.find_all_domains()
        self.httprobe()

    def does_file_exist(self, file_path):
        file = Path(file_path)
        return file.is_file()

    def find_all_domains(self):
        if self.does_file_exist(self.all_domains):
            self.log('Skipping domains-all file generation')
            return

        targets = self.get_probe_targets_files()

        with open(self.all_domains, "w") as outfile:
            cat = subprocess.Popen(['awk', '1'] + targets, stdout=subprocess.PIPE)
            grep_blacklist = subprocess.Popen(['grep', '-v', '-f', self.blacklist_file], stdin=cat.stdout, stdout=subprocess.PIPE)
            sort = subprocess.Popen(['sort', '-u'], stdin=grep_blacklist.stdout, stdout=outfile)
            sort.wait()

    def get_probe_targets_files(self):
        return [
            '{}/domains-all-amass'.format(self.working_dir),
            '{}/domains-brute-massdns'.format(self.working_dir)
        ]

    def httprobe(self):
        with open(self.results, "w") as outfile:
            cat = subprocess.Popen(['cat', self.all_domains], stdout=subprocess.PIPE)
            probe = subprocess.Popen(['httprobe'], stdin=cat.stdout, stdout=subprocess.PIPE)
            sed_0 = subprocess.Popen(['sed', 's/http:\/\///g'], stdin=probe.stdout, stdout=subprocess.PIPE)
            sed_1 = subprocess.Popen(['sed', 's/https:\/\///g'], stdin=sed_0.stdout, stdout=subprocess.PIPE)
            sort = subprocess.Popen(['sort', '-u'], stdin=sed_1.stdout, stdout=outfile)
            sort.wait()
