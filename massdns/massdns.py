import sys
import json
import subprocess

RESOLVERS_PATH = '../../massdns/lists/resolvers.txt'

wordlist = open('../commonspeak').read().split('\n')
domains = open(sys.argv[1]).read().split('\n')


# class MassDns:
#
#     def __init__(self, target, working_dir):



def construct_subdomains(root_domain):
    subdomains = list()
    for word in wordlist:
        if not word.strip():
            continue
        subdomains.append('{}.{}\n'.format(word.strip(), root_domain))

    return subdomains


def _exec_and_readlines(cmd, tagets):
    domains_str = bytes('\n'.join(tagets), 'ascii')
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.PIPE)
    stdout, _ = proc.communicate(input=domains_str)
    return [j.decode('utf-8').strip() for j in stdout.splitlines() if j != b'\n']


def get_massdns(targets):
    massdns_cmd = [
        'massdns',
        '-s', '10000',
        '-t', 'A',
        '-o', 'J',
        '-r', RESOLVERS_PATH,
        '--flush'
    ]

    for line in _exec_and_readlines(massdns_cmd, targets):
        if not line:
            continue

        result = json.loads(line.strip())

        try:
            answers = result['data']['answers']
            print(result['name'][:-1])
        except KeyError:
            continue


for root_domain in domains:
    if not root_domain:
        continue

    subdomains = construct_subdomains(root_domain)
    get_massdns(subdomains)