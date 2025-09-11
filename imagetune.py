import numpy as np 
from functools import wraps
from ui import make_ui
from collections import OrderedDict


_TUNES = OrderedDict()

def tune(func=None, min=None, max=None, name=None):
    def decorator(f):
        @wraps(f)
        def wrapper(im, val):
            name_ = name or f.__name__
            if name_ not in _TUNES:
                # Fill on first call (ensures order is correct):
                _TUNES[name_] = {"name": name_, "func": wrapper, "min": min, "max": max, "value": val, "result": None}

            res = f(im, _TUNES[name_]['value'])
            _TUNES[name_]['result'] = np.array(res)

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

def get_tunes():
    return _TUNES


def tuneui(pipeline, im):
    pipeline(im)
    make_ui(pipeline, im, get_tunes())
