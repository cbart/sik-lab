# -*- coding: utf-8 -*-
'''Terminal client commands.'''

import inspect
import functools
import shlex
import sklab.util.functional as functional
from sklab.view.util import ArgumentError

__maintainer__ = 'Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'
__credits__ = ['Cezary Bartoszuk']


class BaseCommand:

    pass


class ConnCommand(BaseCommand):

    pass


_ADDITIONAL_WORDCHARS = '.+=-'
_OPT_ARG_PREFIX = '--'
_OPT_ARG_INTERFIX = '='


@functional.parameterizable_decorator
def argument_extractor(fn):
    '''Extracts function's arguments.'''

    def arg_is_optional(arg):
        '''Checks whether given argument token is optional.'''

        return arg.startswith(_OPT_ARG_PREFIX)

    def parse_opt_arg(arg):
        '''Returns a pair `name, value` contained with parsed opt arg.'''

        if _OPT_ARG_INTERFIX not in arg[len(_OPT_ARG_PREFIX):]:
            raise ArgumentError("Optional arg `%s` does not contain `%s`."
                    % (arg, _OPT_ARG_INTERFIX))
        return arg[len(_OPT_ARG_PREFIX):].split(_OPT_ARG_INTERFIX, 2)

    @functools.wraps(fn)
    def wrapped(self, line):

        lexer = shlex.shlex(line, None, posix=True)
        lexer.wordchars += _ADDITIONAL_WORDCHARS
        req_given_args = list()
        opt_given_args = dict()
        for token in lexer:
            if arg_is_optional(token):
                name, value = parse_opt_arg(token)
                opt_given_args[name] = value
            else:
                req_given_args.append(token)

        argspec = inspect.getargspec(fn)
        defaults_len = len(argspec.defaults)
        req_fn_arg_names = argspec.args[:-defaults_len]
        opt_fn_arg_names = argspec.args[-defaults_len:]

        # All required arguments should be given.
        if len(req_fn_arg_names) - 1 != len(req_given_args):
            raise ArgumentError("Wrong number of required arguments: " \
                    "%d expected, %d given." % (
                        len(req_fn_arg_names) - 1,
                        len(req_given_args)
                        ))
        # Given optional arguments should be a subset
        # of expected optional arguments.
        if not (set(opt_given_args.keys()) <= set(opt_fn_arg_names)):
            raise ArgumentError("Unexpected optional arguments given: \n" +
                    ', '.join(opt_given_args.keys() - set(opt_fn_arg_names)) +
                    ' ')

        return fn(self, *req_given_args, **opt_given_args)

    return wrapped

