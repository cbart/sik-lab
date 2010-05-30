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


def inject_function_before(to_inject):
    """A decorator, which injects a call to the specified function before the
       decorated method is called.

       Injected function is called with no arguments except self.
    """

    def decorator(fn):
        @functools.wraps(fn)
        def decorated(self, *args, **kwargs):
            to_inject(self)
            return fn(self, *args, **kwargs)
        return decorated
    return decorator


def oneshot(fn):
    """A decorator, which make sure, that the method is called only once (per
       object instance).  Subsequent calls return None without calling the
       decorated function."""

    attr_name = '__%d_called' % id(fn)

    @functools.wraps(fn)
    def decorated(self, *args, **kwargs):
        if attr_name in self.__dict__:
            return None
        self.__dict__[attr_name] = True
        return fn(self, *args, **kwargs)
    decorated._oneshot = True
    decorated._oneshotAttributeName = attr_name

    return decorated


def reset_oneshot(bound_method):
    assert bound_method._oneshot, \
            'Called @reset_oneshot on a non-decorated method'

    self = bound_method.im_self
    self.__dict__.pop(bound_method._oneshotAttributeName, None)


def inject_function_after(to_inject):
    """A decorator, which injects a call to the specified method after the
       decorated method is called.

       Injected method is called with no arguments except self.
    """

    def decorator(fn):
        @functools.wraps(fn)
        def decorated(self, *args, **kwargs):
            ret = fn(self, *args, **kwargs)
            to_inject(self)
            return ret
        return decorated
    return decorator


def memoized(fn):
    """Simple wrapper that adds result caching for argument-less functions."""
    cache = []
    @functools.wraps(fn)
    def memoizer():
        if not cache:
            cache.append(fn())
        return cache[0]
    return memoizer

