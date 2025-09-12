import pytest
from types import SimpleNamespace
from imagetune.helper_functions import add_written_names, _param_list_excl_im, replace_in_args_or_kwargs, resolve_argname, find_in_args_or_kwargs


def f(im, a, b, c=5):
    return im * a + b * c

@pytest.fixture
def spec_good():
    # matches f(im, a, b, c=5)
    return SimpleNamespace(args=['im', 'a', 'b', 'c'])

@pytest.fixture
def spec_empty():
    # "wrong" argspec case you called out
    return SimpleNamespace(args=[])

@pytest.fixture
def spec_none():
    # also ensure robustness to args=None
    return SimpleNamespace(args=None)


# -------------------- _param_list_excl_im ----------------------

def test_param_list_excludes_first_param(spec_good):
    assert _param_list_excl_im(spec_good, None) == ['a', 'b', 'c']

def test_param_list_uses_placeholders_when_argnum_exceeds_length(spec_empty):
    assert _param_list_excl_im(spec_empty, 3) == ['arg1', 'arg2', 'arg3']

def test_param_list_with_argnum_but_sufficient_params_keeps_real_names(spec_good):
    assert _param_list_excl_im(spec_good, 2) == ['a', 'b', 'c']

def test_param_list_handles_none_args(spec_none):
    assert _param_list_excl_im(spec_none, 2) == ['arg1', 'arg2']


# ----------------------- resolve_argname -----------------------

def test_resolve_by_argnum(spec_good):
    assert resolve_argname(spec_good, argnum=2) == 'b'

def test_resolve_by_argname_direct(spec_good):
    assert resolve_argname(spec_good, argname='c') == 'c'

def test_resolve_with_placeholders_when_argspec_empty(spec_empty):
    assert resolve_argname(spec_empty, argnum=2) == 'arg2'

@pytest.mark.parametrize("argnum,argname", [(None, None), (1, 'a')])
def test_resolve_requires_exactly_one_selector(spec_good, argnum, argname):
    with pytest.raises(ValueError):
        resolve_argname(spec_good, argnum=argnum, argname=argname)


# ------------------- find_in_args_or_kwargs --------------------

def test_find_prefers_kwargs_when_present(spec_good):
    args = (2, 3, 7)
    kwargs = {'b': 42}
    assert find_in_args_or_kwargs(spec_good, args, kwargs, argname='b') == 42

def test_find_by_argnum_from_args(spec_good):
    args = (2, 3, 7)  # maps to a=2, b=3, c=7
    kwargs = {}
    assert find_in_args_or_kwargs(spec_good, args, kwargs, argnum=1) == 2

def test_find_by_argname_from_args(spec_good):
    args = (2, 3, 7)
    kwargs = {}
    assert find_in_args_or_kwargs(spec_good, args, kwargs, argname='b') == 3

def test_find_unknown_param_raises_keyerror(spec_good):
    with pytest.raises(KeyError):
        find_in_args_or_kwargs(spec_good, (), {}, argname='does_not_exist')

def test_find_value_missing_raises_keyerror(spec_good):
    # ask for c (idx 2) but provide fewer args and no kwargs
    with pytest.raises(KeyError):
        find_in_args_or_kwargs(spec_good, (1,), {}, argname='c')

def test_find_with_placeholder_params_when_argspec_empty(spec_empty):
    # argnum=2 -> params = ['arg1','arg2']; take from args position 1
    args = (10, 20)
    kwargs = {}
    assert find_in_args_or_kwargs(spec_empty, args, kwargs, argnum=2) == 20

def test_find_requires_exactly_one_selector_value_error(spec_good):
    with pytest.raises(ValueError):
        find_in_args_or_kwargs(spec_good, (), {}, argnum=None, argname=None)
    with pytest.raises(ValueError):
        find_in_args_or_kwargs(spec_good, (), {}, argnum=1, argname='a')


# ------------------ replace_in_args_or_kwargs ------------------

def test_replace_in_kwargs(spec_good):
    args = [2, 3, 7]
    kwargs = {'b': 9}
    replace_in_args_or_kwargs(spec_good, args, kwargs, 99, argname='b')
    assert kwargs['b'] == 99
    assert args == [2, 3, 7]

def test_replace_in_args_by_argnum(spec_good):
    args = [2, 3, 7]
    kwargs = {}
    replace_in_args_or_kwargs(spec_good, args, kwargs, 5, argnum=1)  # replace a
    assert args == [5, 3, 7]
    assert kwargs == {}

def test_replace_in_args_by_argname(spec_good):
    args = [2, 3, 7]
    kwargs = {}
    replace_in_args_or_kwargs(spec_good, args, kwargs, 11, argname='c')
    assert args == [2, 3, 11]

def test_replace_adds_to_kwargs_when_not_found_anywhere(spec_good):
    args = [2]  # only 'a' present positionally
    kwargs = {}
    replace_in_args_or_kwargs(spec_good, args, kwargs, 123, argname='c')
    assert kwargs == {'c': 123}
    assert args == [2]

def test_replace_with_placeholder_params_when_argspec_empty(spec_empty):
    # argnum=3 -> params ['arg1','arg2','arg3']; only one arg provided; should go to kwargs['arg3']
    args = [10]
    kwargs = {}
    replace_in_args_or_kwargs(spec_empty, args, kwargs, 777, argnum=3)
    assert args == [10]
    assert kwargs == {'arg3': 777}

def test_replace_requires_exactly_one_selector_value_error(spec_good):
    with pytest.raises(ValueError):
        replace_in_args_or_kwargs(spec_good, [], {}, 0, argnum=None, argname=None)
    with pytest.raises(ValueError):
        replace_in_args_or_kwargs(spec_good, [], {}, 0, argnum=1, argname='a')


# ----------------------- add_written_names ---------------------

def test_add_written_names_deduplicates_with_suffixes():
    d = {
        'x': {'name': 'alpha'},
        'y': {'name': 'beta'},
        'z': {'name': 'alpha'},
        'w': {'name': 'beta'},
        'u': {'name': 'gamma'},
    }
    out = add_written_names(d)

    # counts: alpha=2, beta=2 -> suffixed; gamma=1 -> unsuffixed
    assert out['x']['written_name'] == 'alpha:1'
    assert out['z']['written_name'] == 'alpha:2'
    assert out['y']['written_name'] == 'beta:1'
    assert out['w']['written_name'] == 'beta:2'
    assert out['u']['written_name'] == 'gamma'

def test_add_written_names_returns_same_object_reference():
    d = {'k': {'name': 'n'}}
    out = add_written_names(d)
    assert out is d  # function mutates and returns the same dict
