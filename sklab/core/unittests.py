# -*- coding: utf-8 -*-
'''Unittests for message_types module.'''

from nose.tools import *
import unittest
from sklab.core import P2PController, ControllerError

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


class TestConnectedAndSignedIn(unittest.TestCase):

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


class TestConnectedButNotSignedIn(unittest.TestCase):

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


class TestNotConnected(unittest.TestCase):

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


class TestRegistrationEnabled(unittest.TestCase):

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


class TestRegistrationDisabled(unittest.TestCase):

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


class TestSendingEnabled(unittest.TestCase):

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


class TestSendingDisabled(unittest.TestCase):

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


class TestReceiveOneMessage(unittest.TestCase):

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


class TestReceiveNoMessages(unittest.TestCase):

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


class TestSignedInShutdown(unittest.TestCase):

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


class TestConnectedButNotSignedInShutdown(unittest.TestCase):

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


class TestDisconnectedShutdown(unittest.TestCase):

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



class RPCClientTest(unittest.TestCase):

    def setUp(self):

        pass
        # mock server stand up

    def tearDown(self):

        pass
        # mock server shut down

#TODO: mock test

if __name__ == '__main__':
    unittest.main()
