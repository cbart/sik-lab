# -*- coding: utf-8 -*-
'''Unittests for message_types module.'''

from nose.tools import *
import unittest
import xmlrpclib

from sklab.core.test_base import TestCase
from sklab.core import P2PController, ControllerError, RPCClient
from sklab.server.core.rpc_server import \
        RPCServer
from sklab.server.core.rpc_mock import \
        RPCMock, _DEFAULT_PORT as _DEFAULT_MOCK_PORT
from sklab.server.util import \
        findPort


__maintainer__ = 'Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'
__credits__ = 'Cezary Bartoszuk'


_TEST_RESULT = '_my_fancy_result_'


class RPCClientMock(object):

    responses = {
            'connect': False,
            'disconnect': True,
            'isConnected': True,
            'singIn': True,
            'signOut': True,
            'isSignedIn': True,
            'registerUser': True,
            'send': True,
            'shutdown': True,
            'receive': [{'from': 'zosia', 'content': 'I love ASD.'}],
            }

    def __init__(self, address,
            connected=True,
            signed_in=True,
            register_success=True,
            send_success=True,
            receive_list=None,
            shutdown_success=True):

        signed_in = signed_in and connected

        self.responses['connect'] = not connected
        self.responses['disconnect'] = connected
        self.responses['isConnected'] = connected

        self.responses['signIn'] = not signed_in
        self.responses['signOut'] = signed_in
        self.responses['isSignedIn'] = signed_in

        self.responses['registerUser'] = register_success

        self.responses['send'] = send_success

        self.responses['shutdown'] = shutdown_success

        if receive_list is not None:
            self.responses['receive'] = receive_list

    def call_action(self, method_name, **kwargs):

        ret_val = self.responses.get(method_name, None)

        # We shutdown only while disconnected and (obviously) not signed in.
        if method_name == 'shutdown':
            ret_val = ret_val and not self.responses.get('isSignedIn', True)
            ret_val = ret_val and not self.responses.get('isConnected', True)
        if method_name == 'signOut':
            self.responses['signIn'] = True
            self.responses['signOut'] = False
            self.responses['isSignedIn'] = False
        if method_name == 'disconnect':
            self.responses['connect'] = True
            self.responses['disconnect'] = False
            self.responses['isConnected'] = False

        return ret_val


_IP = '192.168.0.1'
_PORT = 42

_LOGIN = 'rambo'
_PASSWORD = 'IHaveGreatMuscles'

_CONTENT = '''
        Hi!

        I have heard that your favourite algorithm
        is the Ford-Fulkerson. Have you heard that
        without the Bland rule it can run forever?

        Best regards.
'''


class TestConnectedAndSignedIn(TestCase):

    def setUp(self):

        self.rpc_mock = RPCClientMock('http://false_address:8080')
        self.controller = P2PController(self.rpc_mock)

    @raises(ControllerError)
    def testAssertNotConnected(self):

        self.controller.assertNotConnected()

    def testAssertConnected(self):

        self.controller.assertConnected()

    @raises(ControllerError)
    def testAssertNotSignedIn(self):

        self.controller.assertNotSignedIn()

    def testAssertSignedIn(self):

        self.controller.assertSignedIn()

    @raises(ControllerError)
    def testConnect(self):

        self.controller.connect(_IP, _PORT)

    @raises(ControllerError)
    def testSignIn(self):

        self.controller.signIn(_LOGIN, _PASSWORD)

    def testSignOut(self):

        self.controller.signOut()

    def tearDown(self):

        self.rpc_mock = None
        self.controller = None


class TestConnectedButNotSignedIn(TestCase):

    def setUp(self):

        self.rpc_mock = RPCClientMock('http://false_address:8080',
                signed_in=False)
        self.controller = P2PController(self.rpc_mock)

    @raises(ControllerError)
    def testAssertNotConnected(self):

        self.controller.assertNotConnected()

    def testAssertConnected(self):

        self.controller.assertConnected()

    def testAssertNotSignedIn(self):

        self.controller.assertNotSignedIn()

    @raises(ControllerError)
    def testAssertSignedIn(self):

        self.controller.assertSignedIn()

    @raises(ControllerError)
    def testConnect(self):

        self.controller.connect(_IP, _PORT)

    def testSignIn(self):

        self.controller.signIn(_LOGIN, _PASSWORD)

    @raises(ControllerError)
    def testSignOut(self):

        self.controller.signOut()

    def tearDown(self):

        self.rpc_mock = None
        self.controller = None


class TestNotConnected(TestCase):

    def setUp(self):

        self.rpc_mock = RPCClientMock('http://false_address:8080',
                connected=False)
        self.controller = P2PController(self.rpc_mock)

    def testAssertNotConnected(self):

        self.controller.assertNotConnected()

    @raises(ControllerError)
    def testAssertConnected(self):

        self.controller.assertConnected()

    @raises(ControllerError)
    def testAssertNotSignedIn(self):

        self.controller.assertNotSignedIn()

    @raises(ControllerError)
    def testAssertSignedIn(self):

        self.controller.assertSignedIn()

    def testConnect(self):

        self.controller.connect(_IP, _PORT)

    @raises(ControllerError)
    def testSignIn(self):

        self.controller.signIn(_LOGIN, _PASSWORD)

    @raises(ControllerError)
    def testSignOut(self):

        self.controller.signOut()

    def tearDown(self):

        self.rpc_mock = None
        self.controller = None


class TestRegistrationEnabled(TestCase):

    def setUp(self):

        self.rpc_mock = RPCClientMock('http://false_address:8080',
                connected=True,
                register_success=True)
        self.controller = P2PController(self.rpc_mock)

    def testRegistration(self):

        self.controller.registerUser(_LOGIN, _PASSWORD)

    def tearDown(self):

        self.rpc_mock = None
        self.controller = None


class TestRegistrationDisabled(TestCase):

    def setUp(self):

        self.rpc_mock = RPCClientMock('http://false_address:8080',
                connected=True,
                register_success=False)
        self.controller = P2PController(self.rpc_mock)

    @raises(ControllerError)
    def testRegistration(self):

        self.controller.registerUser(_LOGIN, _PASSWORD)

    def tearDown(self):

        self.rpc_mock = None
        self.controller = None


class TestSendingEnabled(TestCase):

    def setUp(self):

        self.rpc_mock = RPCClientMock('http://false_address:8080',
                signed_in=True,
                connected=True,
                send_success=True)
        self.controller = P2PController(self.rpc_mock)

    def testRegistration(self):

        self.controller.send(_LOGIN, _CONTENT)

    def tearDown(self):

        self.rpc_mock = None
        self.controller = None


class TestSendingDisabled(TestCase):

    def setUp(self):

        self.rpc_mock = RPCClientMock('http://false_address:8080',
                signed_in=True,
                connected=True,
                send_success=False)
        self.controller = P2PController(self.rpc_mock)

    @raises(ControllerError)
    def testRegistration(self):

        self.controller.send(_LOGIN, _CONTENT)

    def tearDown(self):

        self.rpc_mock = None
        self.controller = None


class TestReceiveOneMessage(TestCase):

    def setUp(self):

        self.rpc_mock = RPCClientMock('http://false_address:8080',
                receive_list=[{
                        'from': _LOGIN,
                        'content': _CONTENT
                    }])
        self.controller = P2PController(self.rpc_mock)

    def _assertValidMessage(self, message):

        self.assertTrue(message.has_key('from'))
        self.assertTrue(message.has_key('content'))

    def testRegistration(self):

        messages = self.controller.receive()
        self.assertTrue(messages is not None)
        self.assertTrue(len(messages) > 0)
        for message in messages:
            self._assertValidMessage(message)

    def tearDown(self):

        self.rpc_mock = None
        self.controller = None


class TestReceiveNoMessages(TestCase):

    def setUp(self):

        self.rpc_mock = RPCClientMock('http://false_address:8080',
                receive_list=[])
        self.controller = P2PController(self.rpc_mock)

    def testRegistration(self):

        messages = self.controller.receive()
        self.assertTrue(messages == [])

    def tearDown(self):

        self.rpc_mock = None
        self.controller = None


class TestSignedInShutdown(TestCase):

    def setUp(self):

        self.rpc_mock = RPCClientMock('http://false_address:8080',
                signed_in=True,
                connected=True,
                shutdown_success=True)
        self.controller = P2PController(self.rpc_mock)

    def testShutdown(self):

        self.controller.shutDown()

    def tearDown(self):

        self.rpc_mock = None
        self.controller = None


class TestConnectedButNotSignedInShutdown(TestCase):

    def setUp(self):

        self.rpc_mock = RPCClientMock('http://false_address:8080',
                signed_in=False,
                connected=True,
                shutdown_success=True)
        self.controller = P2PController(self.rpc_mock)

    def testShutdown(self):

        self.controller.shutDown()

    def tearDown(self):

        self.rpc_mock = None
        self.controller = None


class TestDisconnectedShutdown(TestCase):

    def setUp(self):

        self.rpc_mock = RPCClientMock('http://false_address:8080',
                signed_in=False,
                connected=False,
                shutdown_success=True)
        self.controller = P2PController(self.rpc_mock)

    def testShutdown(self):

        self.controller.shutDown()

    def tearDown(self):

        self.rpc_mock = None
        self.controller = None



class TestRPCClient(TestCase):

    _SERVER_HOST = 'localhost'
    _SERVER_PORT = None

    _LOGIN = 'my_secret_login'
    _PASSWORD = 'my_secret_password'
    _IP = '192.168.0.1'
    _PORT = 11381

    def setUp_1999_findFreshPort(self):

        self._SERVER_PORT = findPort()

    def tearDown_1999_findFreshPort(self):

        self._SERVER_PORT = None

    def setUp_2000_rpcServer(self):

        self.rpc_mock_instance = RPCMock()
        self.rpc_server_instance = RPCServer(
                self._SERVER_HOST,
                self._SERVER_PORT,
                self.rpc_mock_instance)
        self.rpc_server_instance.run()

    def tearDown_2000_rpcServer(self):

        self.rpc_client = None
        self.rpc_server_instance.stop()
        self.rpc_server_instance = None
        self.rpc_mock_instance = None

    def setUp_2001_rpcClient(self):

        self.rpc_client = RPCClient(
                "http://%s:%d/" % (self._SERVER_HOST, self._SERVER_PORT))

    def tearDown_2001_rpcClient(self):

        self.rpc_client = None

    def testIsConnected(self):

        self.assertFalse(self.rpc_client.call_action('isConnected'))
        self.assertTrue(self.rpc_client.call_action('connect',
            self._IP, self._PORT))
        self.assertTrue(self.rpc_client.call_action('isConnected'))
        self.assertTrue(self.rpc_client.call_action('disconnect'))
        self.assertFalse(self.rpc_client.call_action('isConnected'))

if __name__ == '__main__':
    unittest.main()
