import json
import os
import subprocess
import sys
import tempfile


def fetch_versions(pn):
    with tempfile.TemporaryDirectory() as tmpdir:
        owd = os.getcwd()
        os.chdir(tmpdir)
        url = 'http://registry.npmjs.org/{}'.format(pn)
        exit_code = subprocess.call(['wget', url], stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)
        if exit_code:
            print('!!! {} not found on npm'.format(pn))
            sys.exit(exit_code)
        with open(pn) as f:
            metadata = json.load(f)
        os.chdir(owd)

    versions = filter(lambda x: '-' not in x,
                      list(metadata['versions'].keys()))

    return(sorted(versions,
                  key=lambda s: list(map(int, s.split('-')[0].split('.')))))


def fetch_metadata(pn, pv):
    pnv = '{}-{}'.format(pn, pv)
    tarball = '{}.tgz'.format(pnv)
    with tempfile.TemporaryDirectory() as tmpdir:
        owd = os.getcwd()
        os.chdir(tmpdir)
        url = 'http://registry.npmjs.org/{}/-/{}'.format(pn, tarball)
        exit_code = subprocess.call(['wget', url], stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)
        if exit_code:
            print('!!! {} not found on npm'.format(pnv))
            sys.exit(exit_code)
        exit_code = subprocess.call(['tar', 'fxz', tarball],
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)
        if exit_code:
            print('!!! failed to untar {}'.format(tarball))
            sys.exit(exit_code)
        with open('package/package.json') as f:
            metadata = json.load(f)
        os.chdir(owd)

    return(metadata)
