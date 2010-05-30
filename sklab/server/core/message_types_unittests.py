# -*- coding: utf-8 -*-
'''Unittests for message_types module.'''

from nose.tools import *
import unittest
import sklab.server.core.message_types as msg

__maintainer__ = 'Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'
__credits__ = 'Cezary Bartoszuk'


_STRINGS = [
        '''''',
        '''Lorem Ipsum''',
        r'''`1234567890-=
           qwertyuiop[]\
           asdfghjkl;'
           zxcvbnm,./
           ~!@#$%^&*()_+
           QWERTYUIOP{}|
           ASDFGHJKL:"
           ZXCVBNM<>?''',
        ''' (THIS_IS_A_SPACE)
           \t(THIS_IS_A_TAB)
           \n(THIS_IS_NEWLINE)
           \r(THIS_IS_CARRIAGE_RET)
           \a(THIS_IS_AN_ALERT)''',
        '''Zażółć gęślą jaźń.''',
        ]

_ARRAYS = [
        [],
        [0],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 3, 2, 1, 8, 7, 6, 5, 9],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        range(0, 1000000, 10000),
        ]

_MSG_HOSTNAMES = [
        '',
        'localhost',
        '192.168.0.1',
        ]

_MSG_PORTS = range(0, 64000, 13451)


class TestTypes(unittest.TestCase):

    def testUInt8(self):

        for i in range(0, 256):
            instance = msg.UInt8(i)
            code = instance.code()
            second_instance, data_left = msg.UInt8.parseHead(code)
            eq_(second_instance.value, instance.value)
            eq_(data_left, '')

    def testUInt32(self):

        for i in range(0, 4294967295, 1000000):
            instance = msg.UInt32(i)
            code = instance.code()
            second_instance, data_left = msg.UInt32.parseHead(code)
            eq_(second_instance.value, instance.value)
            eq_(data_left, '')

    def testVarString(self):

        for string in _STRINGS:
            instance = msg.VarString(string)
            code = instance.code()
            second_instance, data_left = msg.VarString.parseHead(code)
            eq_(second_instance.value, instance.value)
            eq_(data_left, '')

    def testAddressType(self):

        for length in [0, 1, 42, 1576, 3000, 50000, 1000000]:
            for char in ['a', '\n', '%', '\'']:
                hostname = char * length
                for port in [0, 1, 88, 2900]:
                    instance = msg.AddressType(hostname, port)
                    code = instance.code()
                    second_instance, data_left = \
                        msg.AddressType.parseHead(code)
                    eq_(second_instance.hostname, instance.hostname)
                    eq_(second_instance.port, instance.port)
                    eq_(data_left, '')

    def testDataType(self):

        for string in _STRINGS:
            instance = msg.DataType(string)
            code = instance.code()
            second_instance, data_left = msg.DataType.parseHead(code)
            eq_(second_instance.text, instance.text)
            eq_(data_left, '')

    def testIdArrayType(self):

        for array in _ARRAYS:
            instance = msg.IdArrayType(array)
            code = instance.code()
            second_instance, data_left = msg.IdArrayType.parseHead(code)
            eq_(second_instance.intlist, instance.intlist)
            eq_(data_left, '')

    def testMessageAckType(self):

        for i in range(0, 256):
            instance = msg.MessageAckType(i)
            code = instance.code()
            second_instance, data_left = msg.MessageAckType.parseHead(code)
            eq_(second_instance.message_id, instance.message_id)
            eq_(data_left, '')

    def testMessageAddressType(self):

        for i in range(0, 256, 16):
            for hostname in _MSG_HOSTNAMES:
                for port in _MSG_PORTS:
                    instance = msg.MessageAddressType(i,
                            msg.AddressType(hostname, port))
                    code = instance.code()
                    second_instance, data_left = \
                            msg.MessageAddressType.parseHead(code)
                    eq_(second_instance.message_id, instance.message_id)
                    eq_(second_instance.address.hostname,
                            instance.address.hostname)
                    eq_(second_instance.address.port, instance.address.port)
                    eq_(data_left, '')

    def testMessageAddressesType(self):

        for i in [255]:
            for hostname1 in _MSG_HOSTNAMES:
                for hostname2 in _MSG_HOSTNAMES:
                    for port1 in _MSG_PORTS:
                        for port2 in _MSG_PORTS:
                            instance = msg.MessageAddressesType(i,
                                    msg.AddressType(hostname1, port1),
                                    msg.AddressType(hostname2, port2))
                            code = instance.code()
                            second_instance, data_left = \
                                    msg.MessageAddressesType.parseHead(code)
                            eq_(second_instance.message_id, instance.message_id)
                            eq_(second_instance.address1.hostname,
                                    instance.address1.hostname)
                            eq_(second_instance.address1.port,
                                    instance.address1.port)
                            eq_(second_instance.address2.hostname,
                                    instance.address2.hostname)
                            eq_(second_instance.address2.port,
                                    instance.address2.port)
                            eq_(data_left, '')

    def testMessageInfoType(self):

        for i in [0, 123, 255]:
            for hostname in _MSG_HOSTNAMES:
                for port in _MSG_PORTS:
                    for text in _STRINGS:
                        instance = msg.MessageInfoType(i,
                                msg.AddressType(hostname, port),
                                msg.DataType(text))
                        code = instance.code()
                        sec_inst, data_left = \
                                msg.MessageInfoType.parseHead(code)
                        eq_(instance.message_id, sec_inst.message_id)
                        eq_(instance.address.hostname,
                                sec_inst.address.hostname)
                        eq_(instance.address.port,
                                sec_inst.address.port)
                        eq_(instance.data.text,
                                sec_inst.data.text)
                        eq_(data_left, '')

    def testMessageUserType(self):

        for i in [0, 123, 255]:
            for hostname in _MSG_HOSTNAMES:
                for port in _MSG_PORTS:
                    for user in _STRINGS:
                        for password in _STRINGS:
                            instance = msg.MessageUserType(i,
                                    msg.AddressType(hostname, port),
                                    msg.DataType(user),
                                    msg.DataType(password))
                            code = instance.code()
                            sec_inst, data_left = \
                                    msg.MessageUserType.parseHead(code)
                            eq_(instance.message_id, sec_inst.message_id)
                            eq_(instance.address.hostname,
                                    sec_inst.address.hostname)
                            eq_(instance.address.port,
                                    sec_inst.address.port)
                            eq_(instance.login.text,
                                    sec_inst.login.text)
                            eq_(instance.password.text,
                                    sec_inst.password.text)
                            eq_(data_left, '')

    def testMessageMailType(self):

        for i in [0, 123]:
            for hostname in _MSG_HOSTNAMES:
                for port in _MSG_PORTS:
                    for mail_id in [0, 123456, 4535134]:
                        for recipient in ['alfa', 'ceta']:
                            for sender in ['ceta', 'jota']:
                                for content in _STRINGS:
                                    inst = msg.MessageMailType(i,
                                            msg.AddressType(hostname, port),
                                            mail_id,
                                            msg.DataType(recipient),
                                            msg.DataType(sender),
                                            msg.DataType(content))
                                    code = inst.code()
                                    sec_inst, data_left = \
                                        msg.MessageMailType.parseHead(code)
                                    eq_(inst.message_id, sec_inst.message_id)
                                    eq_(inst.address.hostname,
                                            sec_inst.address.hostname)
                                    eq_(inst.address.port,
                                            sec_inst.address.port)
                                    eq_(inst.mail_id, sec_inst.mail_id)
                                    eq_(inst.recipient.text,
                                            sec_inst.recipient.text)
                                    eq_(inst.sender.text, sec_inst.sender.text)
                                    eq_(inst.content.text,
                                            sec_inst.content.text)
                                    eq_(data_left, '')

    def testMessageMailListType(self):

        for i in [0, 255]:
            for hostname in ['local', 'jodie', 'electra']:
                for port in [1, 20, 340, 5500]:
                    for recipient in ['luke', 'vader', 'r2d2']:
                        for messages in _ARRAYS:
                            inst = msg.MessageMailListType(i,
                                    msg.AddressType(hostname, port),
                                    msg.DataType(recipient),
                                    msg.IdArrayType(messages))
                            code = inst.code()
                            sec_inst, data_left = \
                                    msg.MessageMailListType.parseHead(code)
                            eq_(sec_inst.message_id, inst.message_id)
                            eq_(sec_inst.address.hostname,
                                    inst.address.hostname)
                            eq_(sec_inst.address.port, inst.address.port)
                            eq_(sec_inst.recipient.text,
                                    sec_inst.recipient.text)
                            eq_(sec_inst.messages.intlist,
                                    inst.messages.intlist)
                            eq_(data_left, '')


if __name__ == '__main__':
    unittest.main()
