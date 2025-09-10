from functools import wraps
from ui import make_ui


_TUNES = {}

def tune(func=None, **params):
    def decorator(f):
        @wraps(f)
        def wrapper(im, val):
            if _TUNES[f.__name__]['value'] is None:
                _TUNES[f.__name__]['value'] = val
            return f(im, _TUNES[f.__name__]['value'])

        _TUNES[f.__name__] = {"func": wrapper, "params": params, "value": None}
        return wrapper

    if func is None:
        # Case: @tune(min=..., max=...)
        return decorator
    elif callable(func):
        # Case: tune(func, min=..., max=...)
        return decorator(func)
    else:
        raise TypeError("First argument must be callable or None.")

def get_tunes():
    return _TUNES


def tuneui(pipeline, im):
    pipeline(im)
    make_ui(im)
