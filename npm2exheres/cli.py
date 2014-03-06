from npm2exheres.exherbo import create_exheres
from npm2exheres.fetch import fetch_versions, fetch_metadata
from npm2exheres.parse import parse_metadata
from npm2exheres.print import print_msg, print_versions, print_warn
from npm2exheres.validate import (filter_versions, exist_exheres,
                                  validate_params)


__VERSION__ = '0.1.0'


def cli(pn, verspec=None, recursive=False, test=False, unbundle=False,
        messages=[], summary=True):
    if verspec:
        print_msg('Starting {} {}'.format(pn, verspec))
    else:
        print_msg('Starting {}'.format(pn))

    print_msg('Fetching versions of {}'.format(pn))
    versions = fetch_versions(pn)
    print_versions(versions)

    if verspec:
        print_msg('Filtering versions with {}'.format(verspec))
        versions = filter_versions(versions, verspec)
        print_versions(versions)

    pv = versions[-1]
    print_msg('Using version: {}'.format(pv))

    if exist_exheres(pn, pv):
        print_msg('{}-{} exheres exists, skipping'.format(pn, pv))
        return

    print_msg('Fetching {}-{} metadata'.format(pn, pv))
    metadata = fetch_metadata(pn, pv)
    print_msg('Got metadata')
    deps = []
    print_msg('Parsing metadata')
    params = parse_metadata(metadata, deps, test, unbundle)
    print_msg('Done parsing')
    print_msg('Verifying params')
    validate_params(pn, pv, params, messages)
    print_msg('Done verifying')
    print_msg('Writing exheres')
    params['version'] = __VERSION__
    create_exheres(pn, pv, params)
    print_msg('Done writing')

    if recursive:
        n = len(deps)
        for (pn, verspec) in deps:
            print_msg('{}-{}: recursing {} deps'.format(pn, pv, n))
            cli(pn, verspec, recursive, test, unbundle, messages, False)
            n -= 1

    if verspec:
        print_msg('Done with {} {}'.format(pn, verspec))
    else:
        print_msg('Done with {}'.format(pn))

    if summary and len(messages) > 0:
        messages.sort()
        print_msg("Summary of warnings:")
        for message in messages:
            print_warn(message, [])
