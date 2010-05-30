'''Core modules.'''

import xmlrpclib

__maintainer__ = 'Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'
__credits__ = ['Cezary Bartoszuk']


class ControllerError(StandardError):

    pass


class RPCClient(object):

    def __init__(self, address):

        self.server = xmlrpclib.Server(address)

    def call_action(self, method_name, *args, **kwargs):

        res = getattr(self.server, method_name)(*args, **kwargs)
        return res['result']


class P2PController:

    def __init__(self, rpc_client):

        self.rpc_client = rpc_client

    def _call_action(self, method_name, **kwargs):

        return self.rpc_client.call_action(method_name, **kwargs)

    def _is_connected(self):

        return self._call_action('isConnected')

    def _is_signed_in(self):

        return self._call_action('isSignedIn')

    def assertNotConnected(self):

        if self._is_connected():
            raise ControllerError("Already connected")

    def assertConnected(self):

        if not self._is_connected():
            raise ControllerError("Not connected")

    def assertNotSignedIn(self):

        self.assertConnected()
        if self._is_signed_in():
            raise ControllerError("Already signed in")

    def assertSignedIn(self):

        self.assertConnected()
        if not self._is_signed_in():
            raise ControllerError("Not signed in")

    def connect(self, ip, port):

        #TODO: verify ip and port
        self.assertNotConnected()
        success = self._call_action('connect', ip=ip, port=port);
        if not success:
            raise ControllerError("Connection couldn't be established")

    def disconnect(self):

        self.assertConnected()
        success = self._call_action('disconnect')
        if not success:
            raise ControllerError("An error occured while disconnecting")

    def signIn(self, login, password):

        self.assertNotSignedIn()
        success = self._call_action('signIn', login=login, password=password)
        if not success:
            #TODO: more messages eg invalid password
            raise ControllerError("Signing in failed")

    def signOut(self):

        self.assertSignedIn()
        success = self._call_action('signOut')
        if not success:
            raise ControllerError("Signing out failed")

    def registerUser(self, login, password):

        self.assertConnected()
        success = self._call_action('registerUser')
        if not success:
            raise ControllerError("Registering user failed")

    def send(self, addressee, content):

        self.assertSignedIn()
        success = self._call_action('send', login=addressee, content=content)
        if not success:
            raise ControllerError("Sending message failed.")

    def receive(self):

        self.assertSignedIn()
        return self._call_action('receive') or []

    def shutDown(self):

        if self._is_signed_in():
            self.signOut()
        if self._is_connected():
            self.disconnect()
        success = self._call_action('shutdown')
        if not success:
            raise ControllerError("Shutting down failed.")
