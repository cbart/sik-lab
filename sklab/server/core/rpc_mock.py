# -*- coding: utf-8 -*-
'''RPC Server mockup.'''

import functools
from sklab.util.functional import parameterizable_decorator


_DEFAULT_PORT = 8085


@parameterizable_decorator
def packed(fn):

    @functools.wraps(fn)
    def wrapped(*args, **kwargs):

        return {'result': fn(*args, **kwargs)}

    return wrapped


class RPCMock(object):

    def __init__(self):

        super(RPCMock, self).__init__()
        self.connected = False
        self.signed_in = False
        self.new_network = False
        self.server = 1138
        self.port = _DEFAULT_PORT

    def _is_connected(self):

        return self.connected

    def _is_signed_in(self):

        return self._is_connected() and self.signed_in

    @packed
    def connect(self, ip, port):

        result = not self._is_connected()
        self.connected = True
        return result

    @packed
    def disconnect(self):

        result = self._is_connected()
        self.connected = False
        return result

    @packed
    def isConnected(self):

        return self._is_connected()

    @packed
    def signIn(self, login, password):

        result = (not self._is_signed_in()) and self._is_connected()
        self.signed_in = self._is_connected()
        return result

    @packed
    def signOut(self):

        result = self._is_signed_in()
        self.signed_in = False
        return result

    @packed
    def isSignedIn(self):

        return self._is_signed_in()

    @packed
    def setPort(self, port):

        if not self._is_connected():
            self.port = port
        return not self._is_connected()

    @packed
    def getPort(self):

        return self.port

    @packed
    def shutdown(self):

        result = not (self._is_connected() or self._is_signed_in())
        return result

    @packed
    def registerUser(self, friend, login, password):

        return self._is_connected()

    @packed
    def send(self, login, content):

        return self._is_signed_in()

    @packed
    def receive(self):

        if self._is_signed_in():
            return []
        else:
            return None

    @packed
    def createNetwork(self, login, password):

        conditions = not (self._is_signed_in() or self._is_connected())
        conditions = conditions and not self.new_network
        if conditions:
            self.new_network = True
        return conditions



