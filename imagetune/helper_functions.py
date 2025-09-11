def _param_list_excl_im(argspec, argnum):
    a = list(argspec.args or [])
    if a and a[0] == "im":
        a = a[1:]

    if argnum is not None and not (len(a) >= argnum):
        a = [f'arg{i}' for i in range(1, argnum + 1)]

    return a


def resolve_argname(argspec, argnum=None, argname=None):
    params = _param_list_excl_im(argspec, argnum)
    if (argnum is None) == (argname is None):
        raise ValueError("Provide exactly one of argnum or argname")
    return argname if argname is not None else params[argnum - 1]


def find_in_args_or_kwargs(argspec, args, kwargs, argnum=None, argname=None):
    params = _param_list_excl_im(argspec, argnum)

    if (argnum is None) == (argname is None):
        raise ValueError("Provide exactly one of argnum or argname")

    name = argname if argname is not None else params[argnum - 1]
    if name in kwargs:
        return kwargs[name]

    try:
        idx = params.index(name) if argname is not None else argnum - 1
    except ValueError:
        raise KeyError("Unknown parameter: %r" % name)

    if 0 <= idx < len(args):
        return args[idx]

    raise KeyError("Value for %r not found in args or kwargs" % name)


def replace_in_args_or_kwargs(argspec, args, kwargs, new_value, argnum=None, argname=None):
    params = _param_list_excl_im(argspec, argnum)
    if (argnum is None) == (argname is None):
        raise ValueError("Provide exactly one of argnum or argname")

    name = argname if argname is not None else params[argnum - 1]

    if name in kwargs:
        kwargs[name] = new_value
        return

    idx = params.index(name) if argname is not None else argnum - 1
    if 0 <= idx < len(args):
        args[idx] = new_value
        return

    kwargs[name] = new_value


def add_written_names(d):
    counts = {}

    for v in d.values():
        counts[v["name"]] = counts.get(v["name"], 0) + 1
    seen = {}

    for v in d.values():
        n = v["name"]
        seen[n] = seen.get(n, 0) + 1
        v["written_name"] = f"{n}:{seen[n]}" if counts[n] > 1 else n

    return d
