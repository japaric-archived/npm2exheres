from npm2exheres.exherbo import verspec
import os.path


def get_deps(metadata, fields, target, deps_acc, comment=False):
    if comment:
        template = '\n#NPM_' + target + '_DEPS=(\n    #{}\n#)\n'
        glue = '\n    #'
    else:
        template = '\nNPM_' + target + '_DEPS=(\n    {}\n)\n'
        glue = '\n    '

    dpairs = []
    for field in fields:
        if field in metadata and metadata[field]:
            deps = metadata[field]
            dnames = sorted(deps.keys())
            if 'bundledDependencies' in metadata:
                dnames = filter(
                    lambda x: x not in metadata['bundledDependencies'], dnames)
            if 'bundleDependencies' in metadata:
                dnames = filter(
                    lambda x: x not in metadata['bundleDependencies'], dnames)
            dpairs += list(map(lambda x: (x, verspec(deps[x])), dnames))

    if dpairs:
        deps_acc += dpairs

        return template.format(glue.join(map(
            lambda x: '"{} [{}]"'.format(x[0], x[1]) if x[1]
                      else '{}'.format(x[0]), dpairs)))
    else:
        return ''


def get_exparams(metadata):
    exparams = []
    if 'engines' in metadata:
        engines = metadata['engines']
        if isinstance(engines, str):
            exparams.append('node_version="[{}]"'.format(
                verspec(engines.lstrip('node '))))
        elif isinstance(engines, list):
            if 'node' in engines:
                pass
            else:
                engines = list(filter(lambda x: x.startswith('node'), engines))
                if engines:
                    exparams.append(verspec(engines[0].lstrip('node ')))
                else:
                    assert(False)
        elif engines['node'] != '*':
            exparams.append('node_version="[{}]"'.format(
                verspec(engines['node'])))

    if 'bin' in metadata and metadata['bin']:
        exparams.append('has_bin=true')

    if exparams:
        return ' [ {} ]'.format(' '.join(exparams))
    else:
        return ''


def get_homepage(metadata):
    if 'homepage' in metadata:
        return '\nHOMEPAGE="{}"'.format(metadata['homepage'])
    else:
        return ''


def get_licenses(metadata):
    if 'license' in metadata:
        licenses = metadata['license']
    elif 'licenses' in metadata:
        licenses = metadata['licenses']
    else:
        return ''

    if not isinstance(licenses, list):
        licenses = [licenses]

    return ' '.join(map(lambda x: x if isinstance(x, str) else x['type'],
                        licenses))


def get_npm_bins(metadata):
    if 'bin' in metadata and metadata['bin']:
        bins = metadata['bin']

        if isinstance(bins, str):
            bpaths = [metadata['bin'].lstrip('./')]
            bnames = [os.path.basename(bpaths[0])]
        else:
            bnames = metadata['bin'].keys()
            bpaths = map(lambda x: x.lstrip('./'),
                         metadata['bin'].values())

        return '\nNPM_BINS=(\n    {}\n)\n'.format('\n    '.join(
            map(lambda x: '"{} {}"'.format(x[0], x[1]), zip(bnames, bpaths))))
    else:
        return ''


def get_src_test(metadata, restrict):
    if restrict:
        template = '\nRESTRICT="test"\n\nsrc_test() {{\n    edo {}\n}}\n'
    else:
        template = '\nsrc_test() {{\n    edo {}\n}}\n'

    if 'scripts' in metadata and 'test' in metadata['scripts']:
        return template.format(metadata['scripts']['test'])
    else:
        return ''


def get_summary(metadata):
    if 'description' in metadata:
        return metadata['description']
    else:
        return ''


def parse_metadata(metadata, deps_acc=[], test=False):
    params = {}

    params['exparams'] = get_exparams(metadata)
    params['homepage'] = get_homepage(metadata)
    params['licenses'] = get_licenses(metadata)
    params['npm_bins'] = get_npm_bins(metadata)
    params['run_deps'] = get_deps(
        metadata, ['dependencies', 'optionalDependencies'], 'RUN', deps_acc)
    params['src_test'] = get_src_test(metadata, not test)
    params['summary'] = get_summary(metadata)
    if test:
        params['test_deps'] = get_deps(
            metadata, ['devDependencies'], 'TEST', deps_acc, not test)
    else:
        params['test_deps'] = get_deps(
            metadata, ['devDependencies'], 'TEST', [], not test)

    return params
