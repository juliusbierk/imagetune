import numpy as np 
from functools import wraps
from collections import OrderedDict
import inspect

from .ui import make_ui, _build_ui_widget

_TUNES = OrderedDict()
_INFO = {'INDEX' : 0}


def tune(func=None, min=None, max=None, name=None, argnums=None, argnames=None):
    if argnames is not None:
        assert argnums is None, "Only one of (argnums, argnames) can be specified."

    if argnums is None and argnames is None:
        argnums = (1, )

    if argnums is not None:
        if isinstance(argnums, int):
            argnums = (argnums,)

        assert isinstance(argnums, tuple), "`argnums` must be a tuple of integers"
        assert isinstance(argnums[0], int), "`argnums` must be a tuple of integers"
        assert all(x >= 1 for x in argnums), "`argnums` must be larger than zero (first argument should be image)"

    if argnames is not None:
        if isinstance(argnames, str):
            argnames = (argnames,)

        assert isinstance(argnames, tuple), "`argnames` must be a tuple of integers"
        assert isinstance(argnames[0], str), "`argnames` must be a tuple of strings"


    def decorator(f):
        @wraps(f)
        def wrapper(im, *args, **kwargs):
            idx = _INFO["INDEX"]
            name_ = name or f.__name__

            if (name_, idx) not in _TUNES:
                # Fill on first call (ensures order is correct):
                _TUNES[(name_, idx)] = {"name": name_, "func": wrapper, "min": min, "max": max,
                                        "args": list(args), "kwargs": dict(kwargs), "result": None, "index": idx,
                                        "argnums":argnums, "argnames": argnames, "argspec": inspect.getfullargspec(f)}

            res = f(im, *_TUNES[(name_, idx)]['args'], **_TUNES[(name_, idx)]['kwargs'])
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
    make_ui(wrappred, im, _TUNES)


def _tune_ui_widget(pipeline, im):
    def wrappred(im):
        _INFO['INDEX'] = 0
        return pipeline(im)

    wrappred(im)
    return _build_ui_widget(wrappred, im, _TUNES)

