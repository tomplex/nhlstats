import json as _json


def dump(plays, fobj):
    return _json.dump({'plays': plays}, fobj)


def dumps(plays):
    return _json.dumps({'plays': plays})
