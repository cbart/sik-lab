# -*- coding: utf-8 -*-
'''Configuration-related objects'''

import datetime

__maintainer__ = 'Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'
__credits__ = ['Cezary Bartoszuk']


_DEFAULT_PORT = 1138

_TIMEOUT_SECONDS = 10

_TIMESTAMP_YEAR = 1989
_TIMESTAMP_MONTH = 7  # July
_TIMESTAMP_DAY = 12
_TIMESTAMP_HOUR = 12
_TIMESTAMP_MINUTE = 5


class Config:
    '''Application configuration object.'''

    default_port = 1138

    timeout = 10

    timestamp = datetime.datetime(
            year=_TIMESTAMP_YEAR,
            month=_TIMESTAMP_MONTH,
            day=_TIMESTAMP_DAY,
            hour=_TIMESTAMP_HOUR,
            minute=_TIMESTAMP_MINUTE)
