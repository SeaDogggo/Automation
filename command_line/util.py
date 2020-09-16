import os
import sys

from logger.logger import Logger


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        return ''


def get_recon_path():
    try:
        return os.environ['RECON_PATH']
    except KeyError:
        Logger('util').error('RECON_PATH variable not set')
        sys.exit()


def get_project_path():
    try:
        return os.environ['RECON_PROJECT_PATH']
    except KeyError:
        Logger('util').error('RECON_PROJECT_PATH variable not set')
        sys.exit()


def get_smuggler_path():
    try:
        return os.environ['SMUGGLER_PATH']
    except KeyError:
        Logger('util').error('RECON_PROJECT_PATH variable not set')
        sys.exit()
