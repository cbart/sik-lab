# -*- coding: utf-8 -*-
'''Server utils.'''

import socket

__maintainer__ = 'Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'
__credits__ = ['Cezary Bartoszuk']


def findPort():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    return sock.getsockname()[1]

