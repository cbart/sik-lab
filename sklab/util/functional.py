'''Functional programming utilities.'''


import functools


__maintainer__ = 'Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'
__credits__ = ['Cezary Bartoszuk', 'Piotr Findeisen']


def parameterizable_decorator(decorator):
    """
        A handy wrapper around decorators (higher-order decorator) that provied
        automatization for the following usage patterns:

        .. python::

            @my_decorator
            def foo(): pass

            @my_decorator()
            def foo(): pass

            @my_decorator(param1=value1, param2=value2):
            def foo(): pass

        Or even:

        .. python::

            @my_decorator(1, 2, 3)
            def foo(): pass

        All you need is to define ``my_decorator`` as follows (note, that
        ``fn`` must always be your first paramter, but doesn't have to be named
        'fn').

        .. python::

            @parameterizable_decorator
            def my_decorator(fn, arg1, arg2, arg3=None, *args, **kwargs):
                ...
    """
    @functools.wraps(decorator)
    def decorator_wrapper(*args, **kwargs):
        if len(args) == 1 and not kwargs and callable(args[0]):
            return decorator(args[0])
        else:
            return lambda fn: \
                    decorator(*((fn,) + args), **kwargs)

    return decorator_wrapper
