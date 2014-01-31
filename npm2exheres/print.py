def print_err(err):
    print('!!!', err)


def print_msg(msg):
    print('[35;01m===[0m', msg)


def print_versions(versions):
    if len(versions) == 1:
        print_msg('1 version: {}'.format(versions[0]))
    elif len(versions) <= 5:
        print_msg('{} versions: {}'.format(len(versions), ', '.join(versions)))
    else:
        print_msg('{} versions: {}, ..., {}'.format(len(versions), versions[0],
                                                    versions[-1]))


def print_warn(warn, messages):
    messages.append(warn)
    print(' [32;01m*[0m ', warn)
