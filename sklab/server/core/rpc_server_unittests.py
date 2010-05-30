# -*- coding: utf-8 -*-


from nose.tools import *
import unittest
import functools
import xmlrpclib

from sklab.core.test_base import \
        TestCase
from sklab.server.core.rpc_server import \
        RPCServer
from sklab.server.core.rpc_mock import \
        RPCMock, _DEFAULT_PORT as _DEFAULT_MOCK_PORT
from sklab.server.util import \
        findPort
from sklab.server.core.rpc_unittests_generic import \
        TestRPCServerInstanceMixin

__maintainer__ = 'Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'
__credits__ = ['Cezary Bartoszuk']

class UnitRPCServerMixin(object):

    _IP = '192.168.0.1'
    _PORT = 8083

    _FRIEND = 'trautman'
    _LOGIN = 'rambo'
    _PASSWORD = 'IHaveAChainGunInMyPocket'

    _MY_FANCY_PORT = 12345
    _DEFAULT_PORT = _DEFAULT_MOCK_PORT

    _SERVER_HOST = 'localhost'
    _SERVER_PORT = None

    def setUp_1999_findFreshPort(self):

        self._SERVER_PORT = findPort()

    def setUp_2000_makeRPCInstance(self):

        self.rpc_mock_instance = RPCMock()
        self.rpc_server_instance = RPCServer(
                self._SERVER_HOST,
                self._SERVER_PORT,
                self.rpc_mock_instance)
        self.rpc_server_instance.run()
        self.rpc_instance = xmlrpclib.Server(
                "http://%s:%d/" % (self._SERVER_HOST, self._SERVER_PORT))

    def tearDown_2000_trashRPCInstance(self):

        self.rpc_instance = None
        self.rpc_server_instance.stop()
        self.rpc_server_instance = None
        self.rpc_mock_instance = None

    def rpcAssertTrue(self, value):

        self.assertTrue(value.get('result', False))

    def rpcAssertFalse(self, value):

        self.assertTrue(not value.get('result', True))

    def rpcAssertEmptyList(self, value):

        self.assertEquals(value.get('result', None), [])

    def rpcAssertNone(self, value):

        something = 'SOMETHING'
        self.assertTrue(value.get('result', something) is None)


class TestRPCServerInstance(
        TestCase,
        TestRPCServerInstanceMixin,
        UnitRPCServerMixin):

    pass


if __name__ == '__main__':
    unittest.main()

