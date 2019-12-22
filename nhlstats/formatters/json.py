import json as _json


def dump(plays, fobj):
    return _json.dump({'data': plays}, fobj)


def dumps(plays):
    return _json.dumps({'data': plays})
