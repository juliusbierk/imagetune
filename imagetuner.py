from functools import wraps
from ui import make_ui


_TUNES = {}

def tune(func=None, min=None, max=None, name=None):
    def decorator(f):
        @wraps(f)
        def wrapper(im, val):
            name_ = name or f.__name__

            if _TUNES[name_]['value'] is None:
                _TUNES[name_]['value'] = val

            return f(im, _TUNES[name_]['value'])

        name_ = name or f.__name__
        if name_ not in _TUNES:
            _TUNES[name_] = {"name": name_, "func": wrapper, "min": min, "max": max, "value": None}

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
