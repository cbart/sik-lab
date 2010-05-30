'''Core modules.'''

from sklib.util.functional import memoized
import xmlrpclib

__maintainer__ = 'Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'
__credits__ = ['Cezary Bartoszuk']


class ControllerError(StandardError):

    pass


class RPCClient(object):

    def __init__(self, address):

        self.server = xmlrpclib.Server(address)

    def call_action(method_name, **kwargs):

        rpc_remote_object = getattr(self.server, self.object_name)
        res = getattr(rpc_remote_object, method_name)(**kwargs)
        return res['result']


class P2PController:

    def __init__(self, rpc_client):

        self.rpc_client = rpc_client

    def _call_action(method_name, **kwargs):

        return self.rpc_client.call_action(method_name, **kwargs)

    def assertNotConnected(self):

        if self._call_action('isConnected'):
            raise ControllerError("Already connected")

    def assertConnected(self):

        if not self._call_action('isConnected'):
            raise ControllerError("Not connected")

    def assertNotSignedIn(self):

        if self.userdata is not None:
            raise ControllerError("Already signed in")

    def assertSignedIn(self):

        if self.userdata is None:
            raise ControllerError("Not signed in")

    #TODO
    def connect(self, ip, port):

        self.connection = 1
