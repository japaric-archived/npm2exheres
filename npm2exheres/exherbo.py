import datetime
import os.path
import re
import subprocess


def create_exheres(pn, pv, params):
    template = """# Copyright {year} {author}
# Generated by npm2exheres-{version}
# Distributed under the terms of the GNU General Public License v2
{run_deps}{test_deps}{npm_bins}
require npm{exparams}

SUMMARY="{summary}"{homepage}

LICENCES="{licenses}"
SLOT="{slot}"
PLATFORMS="~amd64"
{src_test}
"""
    exheres_directory = pn
    exheres_path = '{}/{}-{}.exheres-0'.format(pn, pn, pv)

    params['year'] = datetime.date.today().year
    params['author'] = subprocess.check_output(['git', 'config', '--get',
                                                'user.name'])
    params['author'] = params['author'].decode('utf-8').rstrip('\n')
    params['slot'] = pv

    contents = template.format(**params)

    if not os.path.exists(exheres_directory):
        os.mkdir(exheres_directory)

    with open(exheres_path, 'w') as f:
        f.write(contents)


def verspec(npm_verspec):
    npm_verspec = npm_verspec.lower()

    if npm_verspec == '*':
        return ''
    elif npm_verspec == '':
        return ''
    elif re.match('^[~>=<]*[0-9\.x]+ ', npm_verspec):
        tmp = npm_verspec.partition(' ')
        return verspec(tmp[0]) + '&' + verspec(tmp[2])
    elif re.match('^[0-9]+\.[0-9]+.[0-9]+$', npm_verspec):
        return '=' + npm_verspec
    elif re.match('^[>=<]+[0-9]+\.[0-9]+.[0-9]+$', npm_verspec):
        return npm_verspec
    elif re.match('^[0-9\.]+-[0-9\.]+', npm_verspec):
        return '>=' + npm_verspec.replace('-', '&<=')
    elif re.match('^[0-9]+$', npm_verspec):
        return '~>' + npm_verspec + '.0'
    elif re.match('^[0-9]+\.[0-9]+$', npm_verspec):
        return '~>' + npm_verspec + '.0'
    elif re.match('^[0-9\.]+\.x$', npm_verspec):
        return '~>' + npm_verspec.replace('x', '0')
    elif re.match('^[0-9]+\.x\.x$', npm_verspec):
        return '~>' + npm_verspec.rstrip('.x') + '.0'
    elif re.match('^~[0-9]+$', npm_verspec):
        return '~>' + npm_verspec.lstrip('~') + '.0'
    elif re.match('^~[0-9]+\.[0-9]+$', npm_verspec):
        return '~>' + npm_verspec.lstrip('~') + '.0'
    elif re.match('^~[0-9]+\.[0-9]+\.[0-9]+$', npm_verspec):
        return '~>' + npm_verspec.lstrip('~')
    elif re.match('^[>=<]+[0-9\.]+$', npm_verspec):
        return npm_verspec
    # here be lols
    elif re.match('^[~>=<]+ [0-9\.]+', npm_verspec):
        tmp = npm_verspec.partition(' ')
        return verspec(tmp[0] + tmp[2])
    elif re.match('^~[0-9]+\.[0-9]+\.x$', npm_verspec):
        return '~>' + npm_verspec.lstrip('~').replace('x', '0')
    elif re.match('^=[0-9\.]+x$', npm_verspec):
        return '~>' + npm_verspec.lstrip('=').replace('x', '0')
    # here be wtfs
    elif re.match('^>=[0-9\.]+.x$', npm_verspec):
        return npm_verspec.replace('x', '0')
    else:
        print(npm_verspec)
        assert(False)
