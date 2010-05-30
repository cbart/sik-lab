# -*- coding: utf-8 -*-
'''RPC Server Generic Unittests.'''

from nose.tools import *
import unittest
import functools
from sklab.util.functional import parameterizable_decorator


@parameterizable_decorator
def connect(fn):

    @functools.wraps(fn)
    def wrapped(self, *args, **kwargs):

        self.rpc_instance.connect(self._IP, self._PORT)
        result = fn(self, *args, **kwargs)
        self.rpc_instance.disconnect()

        return result

    return wrapped


@parameterizable_decorator
def sign_in(fn):

    @functools.wraps(fn)
    @connect
    def wrapped(self, *args, **kwargs):

        self.rpc_instance.signIn(self._LOGIN, self._PASSWORD)
        result = fn(self, *args, **kwargs)
        self.rpc_instance.signOut()

        return result

    return wrapped


class TestRPCConnectAndDisconnect(object):

    def testConnectAndDisconnect(self):

        self.rpcAssertTrue(self.rpc_instance.connect(self._IP, self._PORT))
        self.rpcAssertTrue(self.rpc_instance.disconnect())


class TestRPCIsConnected(object):

    def testIsConnectedMethodWhileDisconnected(self):

        self.rpcAssertFalse(self.rpc_instance.isConnected())

    @connect
    def testIsConnectedMethodWhileConnectedButNotSignedIn(self):

        self.rpcAssertTrue(self.rpc_instance.isConnected())

    @sign_in
    def testIsConnectedWhileSignedIn(self):

        self.rpcAssertTrue(self.rpc_instance.isConnected())


class TestRPCSignInAndSignOut(object):

    def testSignInWhileDisconnected(self):

        self.rpcAssertFalse(self.rpc_instance.signIn(self._LOGIN,
            self._PASSWORD))

    def testSignOutWhileDisconnected(self):

        self.rpcAssertFalse(self.rpc_instance.signOut())

    @connect
    def testSignOutWhileConnectedWithoutSignIn(self):

        self.rpcAssertFalse(self.rpc_instance.signOut())

    @connect
    def testSignInAndSignOut(self):

        self.rpcAssertTrue(self.rpc_instance.signIn(self._LOGIN,
            self._PASSWORD))
        self.rpcAssertTrue(self.rpc_instance.signOut())


class TestRPCIsSignedIn(object):

    def testIsSignedInWhileDisconnected(self):

        self.rpcAssertFalse(self.rpc_instance.isSignedIn())

    @connect
    def testIsSignedInWhileConnectedButNotSignedIn(self):

        self.rpcAssertFalse(self.rpc_instance.isSignedIn())

    @sign_in
    def testIsSignedInWhileSignedIn(self):

        self.rpcAssertTrue(self.rpc_instance.isSignedIn())

    # setPort:

    def testSetPortWhileDisconnected(self):

        self.rpcAssertTrue(self.rpc_instance.setPort(self._MY_FANCY_PORT))
        getPort_result = self.rpc_instance.getPort()
        self.assertEquals(getPort_result.get('result', -1),
                self._MY_FANCY_PORT)

    @connect
    def testSetPortWhileConnected(self):

        self.rpcAssertFalse(self.rpc_instance.setPort(self._MY_FANCY_PORT))
        getPort_result = self.rpc_instance.getPort()
        self.assertEquals(getPort_result.get('result', -1),
                self._DEFAULT_PORT)

    # shutdown:

    def testShutdownWhileNotConnected(self):

        self.rpcAssertTrue(self.rpc_instance.shutdown())

    @connect
    def testShutdownWhileConnectedButNotSignedIn(self):

        self.rpcAssertFalse(self.rpc_instance.shutdown())

    @sign_in
    def testShutdownWhileSignedIn(self):

        self.rpcAssertFalse(self.rpc_instance.shutdown())


class TestRPCRegisterUser(object):

    def testRegisterUserWhileNotConnected(self):

        self.rpcAssertFalse(self.rpc_instance.registerUser(
                self._FRIEND, self._LOGIN, self._PASSWORD))

    @connect
    def testRegisterUserWhileConnectedButNotSignedIn(self):

        self.rpcAssertTrue(self.rpc_instance.registerUser(
                self._FRIEND, self._LOGIN, self._PASSWORD))

    @sign_in
    def testRegisterUserWhileSignedIn(self):

        self.rpcAssertTrue(self.rpc_instance.registerUser(
                self._FRIEND, self._LOGIN, self._PASSWORD))


class TestRPCReceive(object):

    def testReceiveWhileNotConnected(self):

        self.rpcAssertNone(self.rpc_instance.receive())

    @connect
    def testReceiveWhileConnectedButNotSignedIn(self):

        self.rpcAssertNone(self.rpc_instance.receive())

    @sign_in
    def testReceiveWhileSignedIn(self):

        self.rpcAssertEmptyList(self.rpc_instance.receive())


class TestRPCCreateNetwork(object):

    def testCreateNewNetwork(self):

        self.rpcAssertTrue(self.rpc_instance.createNetwork(self._LOGIN,
            self._PASSWORD))

    @connect
    def testCreateNewNetworkWhileConnected(self):

        self.rpcAssertFalse(self.rpc_instance.createNetwork(self._LOGIN,
            self._PASSWORD))

    def testDoubleCreateNewNetwork(self):

        self.rpcAssertTrue(self.rpc_instance.createNetwork(self._LOGIN,
            self._PASSWORD))
        self.rpcAssertFalse(self.rpc_instance.createNetwork(self._LOGIN,
            self._PASSWORD))


class TestRPCServerInstanceMixin(
        TestRPCConnectAndDisconnect,
        TestRPCIsConnected,
        TestRPCSignInAndSignOut,
        TestRPCIsSignedIn,
        TestRPCRegisterUser,
        TestRPCReceive,
        TestRPCCreateNetwork):

    pass
