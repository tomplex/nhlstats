__author__ = 'tcaruso'

from itertools import chain as _chain


def _sanitize(value):
    return str(value) if value is not None else ''


def _create_line(values, separator):
    return separator.join(_sanitize(val) for val in values)


def dump(plays, fobj, seperator=','):
    fobj.write(dumps(plays, seperator=seperator))


def dumps(plays, seperator=','):
    header = seperator.join(plays[0].keys())
    rows = (_create_line(play.values(), seperator) for play in plays)

    return '\n'.join(_chain([header], rows))
