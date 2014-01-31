from npm2exheres.print import print_warn
import os


def exist_exheres(pn, pv):
    exheres_path = '{}/{}-{}.exheres-0'.format(pn, pn, pv)
    return os.path.exists(exheres_path)


def filter_versions(versions, verspec):
    """
    >>> filter_versions(['1.2.2', '1.2.3', '1.2.4', '1.3'], '~>1.2.3')
    ['1.2.3', '1.2.4']
    """
    (min_version, max_version) = verspec_to_minmax(verspec)

    return list(filter(lambda v: lte(v, max_version) and gte(v, min_version),
                       versions))


def gte(this, that):
    """
    >>> gte('1.2.3', None)
    True
    >>> gte('1.3.1', [1,3,0])
    True
    >>> gte('1.3', [1,3,0])
    True
    >>> gte('1.3', (1,3,0))
    False
    """
    if not that:
        return True

    this = list(map(int, this.split('.')))

    while len(this) < 3:
        this.append(0)

    if isinstance(that, list):
        return this >= that
    else:
        return this > list(that)


def lte(this, that):
    """
    >>> lte('1.2.3', None)
    True
    >>> lte('1.2.9', [1,3,0])
    True
    >>> lte('1.3', [1,3,0])
    True
    >>> lte('1.3', (1,3,0))
    False
    """
    if not that:
        return True

    this = list(map(int, this.split('.')))

    while len(this) < 3:
        this.append(0)

    if isinstance(that, list):
        return this <= that
    else:
        return this < list(that)


def valid_licenses():
    return os.listdir('/var/db/paludis/repositories/arbor/licences')


def validate_license(license):
    """
    >>> validate_license('BSD-3')
    True
    >>> validate_license('GPL-3')
    True
    >>> validate_license('MIT')
    True
    >>> validate_license('MIT/X11')
    False
    """
    return license in valid_licenses()


def validate_params(pn, pv, params, messages):
    if not params['licenses']:
        print_warn('{}-{}: missing license'.format(pn, pv), messages)
    else:
        licenses = params['licenses'].split(' ')
        for license in licenses:
            if not validate_license(license):
                print_warn('{}-{}: unknown license {}'.format(pn, pv, license),
                           messages)

    if not params['summary']:
        print_warn('{}-{}: missing summary'.format(pn, pv), messages)
    elif len(params['summary']) > 70:
        print_warn('{}-{}: summary is too long'.format(pn, pv), messages)


def verspec_to_minmax(verspec):
    """
    >>> verspec_to_minmax('~>1.2.3')
    ([1, 2, 3], (1, 3, 0))
    >>> verspec_to_minmax('~>1.2')
    ([1, 2, 0], (2, 0, 0))
    >>> verspec_to_minmax('<1.2.3')
    (None, (1, 2, 3))
    """
    if '&' in verspec:
        [min_v, max_v] = verspec.split('&')
        if '~' in min_v:
            verspec = min_v
        elif '~' in max_v:
            verspec = max_v
        else:
            verspec = ''

    if verspec.startswith('~>'):
        min_v = list(map(int, verspec.lstrip('~>').split('.')))
        max_v = min_v[0:-1]
        max_v[-1] += 1
        min_open = False
        max_open = True
    elif verspec.startswith('='):
        min_v = verspec
        max_v = verspec
    elif verspec.startswith('>'):
        min_v = verspec
        max_v = None
    elif verspec.startswith('<'):
        min_v = None
        max_v = verspec

    if min_v:
        if isinstance(min_v, str):
            min_open = not '=' in min_v
            min_v = list(map(int, min_v.lstrip('>=').split('.')))

        while len(min_v) < 3:
            min_v.append(0)

        if min_open:
            min_v = tuple(min_v)

    if max_v:
        if isinstance(max_v, str):
            max_open = not '=' in max_v
            max_v = list(map(int, max_v.lstrip('<=').split('.')))

        while len(max_v) < 3:
            max_v.append(0)

        if max_open:
            max_v = tuple(max_v)

    return (min_v, max_v)
