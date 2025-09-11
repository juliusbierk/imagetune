import numpy as np 
from functools import wraps
from ui import make_ui
from collections import OrderedDict


_TUNES = OrderedDict()
_INFO = {'INDEX' : 0}


def add_written_names(d):
    counts = {}

    for v in d.values():
        counts[v["name"]] = counts.get(v["name"], 0) + 1
    seen = {}

    for v in d.values():
        n = v["name"]
        seen[n] = seen.get(n, 0) + 1
        v["written_name"] = f"{n} {seen[n]}" if counts[n] > 1 else n

    return d

def tune(func=None, min=None, max=None, name=None):
    def decorator(f):
        @wraps(f)
        def wrapper(im, val):
            idx = _INFO["INDEX"]
            name_ = name or f.__name__

            if (name_, idx) not in _TUNES:
                # Fill on first call (ensures order is correct):
                _TUNES[(name_, idx)] = {"name": name_, "func": wrapper, "min": min, "max": max, "value": val, "result": None, "index": idx}

            res = f(im, _TUNES[(name_, idx)]['value'])
            _TUNES[(name_, idx)]['result'] = np.array(res)
            _INFO['INDEX'] += 1

            return res    

        return wrapper

    if func is None:
        # Case: @tune(min=..., max=...)
        return decorator
    elif callable(func):
        # Case: tune(func, min=..., max=...)
        return decorator(func)
    else:
        raise TypeError("Incorrect use of `tune` decorator.")


def tuneui(pipeline, im):
    def wrappred(im):
        _INFO['INDEX'] = 0
        return pipeline(im)

    wrappred(im)
    add_written_names(_TUNES)
    make_ui(wrappred, im, _TUNES)
