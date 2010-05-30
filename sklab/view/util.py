# -*- coding: utf-8 -*-
'''Utilities for terminal view.'''

import functools
import shlex
import sklab.util.functional as functional
from sklab.core import ControllerError

__maintainer__ = 'Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'
__credits__ = ['Cezary Bartoszuk']

__all__ = ['argument_extractor',
        'ArgumentError',
        'error_handler']


class ArgumentError(StandardError):
    '''Exception raised when an error with command argument occurs.'''

    pass


@functional.parameterizable_decorator
def error_handler(fn):
    '''Handles `ArgumentError`s by calling `self._error`.'''

    @functools.wraps(fn)
    def wrapped(self, *args, **kwargs):
        try:
            fn(self, *args, **kwargs)
        except (ArgumentError, ControllerError) as e:
            self._error(str(e))
        except NotImplementedError as nie:
            print "Method is not implemented yet."

    return wrapped


def is_valid_ipv4(ip):
    """Validates IPv4 addresses."""
    pattern = re.compile(r'''
        ^
        (?:
          # Dotted variants:
          (?:
            # Decimal 1-255 (no leading 0's)
            [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
          |
            0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
          |
            0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
          )
          (?:                  # Repeat 0-3 times, separated by a dot
            \.
            (?:
              [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
            |
              0x0*[0-9a-f]{1,2}
            |
              0+[1-3]?[0-7]{0,2}
            )
          ){0,3}
        |
          0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
        |
          0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
        |
          # Decimal notation, 1-4294967295:
          429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
          42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
          4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
        )
        $
    ''', re.VERBOSE | re.IGNORECASE)
    return pattern.match(ip) is not None



