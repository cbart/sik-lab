# -*- coding: utf-8 -*-
'''Model representation.'''

__maintainer__ = 'Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'
__credits__ = ['Cezary Bartoszuk']


class SocketModel(object):

    def __init__(self, ip, port):
        object.__init__(self)
        self.ip = ip
        self.port = port

class NetworkModel:

    pass
