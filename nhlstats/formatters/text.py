import tabulate


def dumps(plays, **kwargs):
    return tabulate.tabulate(plays, headers='keys', **kwargs)


def dump(plays, fobj):
    fobj.write(dumps(plays))
