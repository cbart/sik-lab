# -*- coding: utf-8 -*-
'''RPC Server mockup unittests.'''

from nose.tools import *
import unittest
import functools

from sklab.core.test_base import TestCase
from sklab.server.core.rpc_mock import \
        RPCMock, _DEFAULT_PORT as _DEFAULT_MOCK_PORT
from sklab.server.core.rpc_unittests_generic import \
        TestRPCServerInstanceMixin


__maintainer__ = 'Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'
__credits__ = ['Cezary Bartoszuk']


class UnitRPCMockMixin(object):

    _IP = '192.168.0.1'
    _PORT = 8083

    _FRIEND = 'trautman'
    _LOGIN = 'rambo'
    _PASSWORD = 'IHaveAChainGunInMyPocket'

    _MY_FANCY_PORT = 12345
    _DEFAULT_PORT = _DEFAULT_MOCK_PORT


    def setUp_2000_makeRPCInstance(self):

        self.rpc_instance = RPCMock()

    def tearDown_2000_trashRPCInstance(self):

        self.rpc_instance = None

    def rpcAssertTrue(self, value):

        self.assertTrue(value.get('result', False))

    def rpcAssertFalse(self, value):

        self.assertTrue(not value.get('result', True))

    def rpcAssertEmptyList(self, value):

        self.assertEquals(value.get('result', None), [])

    def rpcAssertNone(self, value):

        something = 'SOMETHING'
        self.assertTrue(value.get('result', something) is None)


class TestRPCMockInstance(
        TestCase,
        TestRPCServerInstanceMixin,
        UnitRPCMockMixin):

    pass


if __name__ == '__main__':
    unittest.main()
