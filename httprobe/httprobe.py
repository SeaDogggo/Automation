import subprocess
from pathlib import Path


class HttProbe:

    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.results = '{}/domains-probed'.format(working_dir)
        self.unique_domains = '{}/domains-all'.format(working_dir)

    def run_all(self):
        self.log('Starting httprobe jobs')
        self.run_httprobe()
        self.log('Finished httprobe jobs')

    def log(self, msg):
        print('[+] {}'.format(msg))

    def run_httprobe(self):
        if self.has_httprobe_run_today(self.results):
            self.log('Skipping httprobe')
            return

        self.find_unique_domains()
        self.httprobe()

    def has_httprobe_run_today(self, scan_results):
        domain_file = Path(scan_results)
        return domain_file.is_file()

    def find_unique_domains(self):
        targets = self.get_probe_targets_files()

        with open(self.unique_domains, "w") as outfile:
            cat_cmd = ['cat'] + targets
            cat = subprocess.Popen(cat_cmd, stdout=subprocess.PIPE)
            sort = subprocess.Popen(['sort', '-u'], stdin=cat.stdout, stdout=outfile)
            sort.wait()

    def get_probe_targets_files(self):
        return [
            '{}/domains-all-amass'.format(self.working_dir),
            '{}/domains-brute-massdns'.format(self.working_dir)
        ]

    def httprobe(self):
        with open(self.results, "w") as outfile:
            cat = subprocess.Popen(['cat', self.unique_domains], stdout=subprocess.PIPE)
            probe = subprocess.Popen(['httprobe'], stdin=cat.stdout, stdout=subprocess.PIPE)
            sed_0 = subprocess.Popen(['sed', 's/http:\/\///g'], stdin=probe.stdout, stdout=subprocess.PIPE)
            sed_1 = subprocess.Popen(['sed', 's/https:\/\///g'], stdin=sed_0.stdout, stdout=subprocess.PIPE)
            sort = subprocess.Popen(['sort', '-u'], stdin=sed_1.stdout, stdout=outfile)
            sort.wait()
