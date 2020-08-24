import os
import sys
from pathlib import Path
from datetime import datetime
from amass.amass import Amass
from massdns.massdns import MassDns
from httprobe.httprobe import HttProbe


class Master:

    target = str()
    working_dir = str()

    def __init__(self):
        self.run()

    def run(self):
        self.parse_args()
        if not self.target:
            self.log('Provide target with -t')
            return

        Amass(self.target, self.working_dir).run_all()
        MassDns('./{}/domains-all-amass'.format(self.working_dir), self.working_dir).run_all()
        HttProbe(self.working_dir).run_all()

    def parse_args(self):
        for i, arg in enumerate(sys.argv):
            if arg == '-t':
                self.set_working_dir(i)

    def set_working_dir(self, i):
        source = self.get_automation_source()
        if not source:
            self.log('AUTOMATION_SOURCE variable not set')
            return

        self.target = sys.argv[i + 1]
        self.working_dir = '{}/{}/{}'.format(source, self.target, datetime.today().strftime('%d-%m-%Y'))
        self.mkdir(self.working_dir)

    def get_automation_source(self):
        try:
            return os.environ['AUTOMATION_SOURCE']
        except KeyError:
            return ''

    def mkdir(self, name):
        Path(name).mkdir(parents=True, exist_ok=True)

    def log(self, msg):
        print('[+] {}'.format(msg))


Master()
