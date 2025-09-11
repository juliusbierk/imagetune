def _param_list_excl_im(argspec):
    a = list(argspec.args or [])
    if a and a[0] == "im":
        a = a[1:]
    return a


def resolve_argname(argspec, argnum=None, argname=None):
    params = _param_list_excl_im(argspec)
    if (argnum is None) == (argname is None):
        raise ValueError("Provide exactly one of argnum or argname")
    return argname if argname is not None else params[argnum]


def find_in_args_or_kwargs(argspec, args, kwargs, argnum=None, argname=None):
    params = _param_list_excl_im(argspec)
    if (argnum is None) == (argname is None):
        raise ValueError("Provide exactly one of argnum or argname")

    name = argname if argname is not None else params[argnum]
    if name in kwargs:
        return kwargs[name]

    try:
        idx = params.index(name) if argname is not None else argnum
    except ValueError:
        raise KeyError("Unknown parameter: %r" % name)

    if 0 <= idx < len(args):
        return args[idx]

    raise KeyError("Value for %r not found in args or kwargs" % name)


def replace_in_args_or_kwargs(argspec, args, kwargs, new_value, argnum=None, argname=None):
    params = _param_list_excl_im(argspec)
    if (argnum is None) == (argname is None):
        raise ValueError("Provide exactly one of argnum or argname")

    name = argname if argname is not None else params[argnum]

    if name in kwargs:
        kwargs[name] = new_value
        return

    idx = params.index(name) if argname is not None else argnum
    if 0 <= idx < len(args):
        args[idx] = new_value
        return

    kwargs[name] = new_value