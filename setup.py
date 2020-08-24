import sys

from command_line.util import get_recon_path
from file.util import mkdir, touch
from logger.logger import Logger


class Setup:

    def __init__(self):
        self.logger = Logger('Setup')
        self.root = get_recon_path()
        self.target = self.parse_args()
        self.validate_target()

    def validate_target(self):
        if not self.target:
            self.logger.error('Need target, use -t')
            sys.exit()

        target_root = '{}/library/{}'.format(self.root, self.target)
        mkdir(target_root)
        mkdir('{}/config'.format(target_root))
        mkdir('{}/config/blacklists'.format(target_root))
        touch('{}/config/blacklists/massdns'.format(target_root))
        touch('{}/config/blacklists/httprobe'.format(target_root))

    def parse_args(self):
        for i, arg in enumerate(sys.argv):
            if arg == '-t':
                return sys.argv[i + 1]


Setup()
