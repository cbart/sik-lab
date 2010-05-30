# -*- coding: utf-8 -*-
'''Message types representation.'''

import struct

__maintainer__ = 'Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'
__credits__ = ['Cezary Bartoszuk']


_ORDER = {
        'NATIVE': '=',
        'BIG': '>',
        'LITTLE': '<',
        'NETWORK': '!',
        }


_STRUCT_TYPE = {
        'CHAR': 'c',
        'SIGNED CHAR': 'b',
        'UNSIGNED CHAR': 'B',
        'SHORT': 'h',
        'UNSIGNED SHORT': 'H',
        'INT': 'i',
        'UNSIGNED INT': 'I',
        'LONG': 'l',
        'UNSIGNED LONG': 'L',
        'LONG LONG': 'q',
        'UNSIGNED LONG LONG': 'Q',
        'OCTET': 's',
        }


_BYTES = {
        'CHAR': 1,
        'UNSIGNED CHAR': 1,
        'SHORT': 2,
        'UNSIGNED SHORT': 2,
        'INT': 4,
        'UNSIGNED INT': 4,
        'LONG': 4,
        'UNSIGNED LONG': 4,
        'LONG LONG': 8,
        'UNSIGNED LONG LONG': 8,
        'OCTET': 1,
        }


def _set_order(order):
    if _ORDER.has_key(order):
        order = _ORDER[order]
    else:
        order = _ORDER['LITTLE']
    return order


def _parse_head(data, type, times=1, order=None):
    '''Returns pair of parsed head (with given type)
       and data without parsed head.

       Default order is Little Endian.
    '''

    order = _set_order(order)
    length = _BYTES[type] * times
    struct_type = _STRUCT_TYPE[type]
    if times > 1:
        struct_type = str(times) + struct_type
    struct_type = order + struct_type
    struct_obj = struct.Struct(struct_type)
    if length > 0:
        return struct_obj.unpack(data[:length])[0], data[length:]
    else:
        return '', data


def _code(instance, type, times=1, order=None):
    '''Returns byte coded `instance`.'''

    order = _set_order(order)
    struct_type = _STRUCT_TYPE[type]
    if times > 1:
        struct_type = str(times) + struct_type
    struct_type = order + struct_type
    struct_obj = struct.Struct(struct_type)
    return struct_obj.pack(instance)


class BaseType(object):
    '''Base structure type.'''

    pass


class BigEndianMixin(object):

    order = 'BIG'


class SingleType(BaseType):
    '''Atomic type.'''

    def __init__(self, value, order=None):

        BaseType.__init__(self)
        self.value = value
        if order is not None:
            self.order = order

    @classmethod
    def parseHead(cls, data, order=None):
        '''Parses data head and returns a pair of:
           parsed string and rest of the data.
        '''

        order = order or cls.order
        value, data = _parse_head(data, type=cls.type, order=order)
        return cls(value), data

    def code(self):
        '''Creates C data of given `instance`.'''

        return _code(self.value, type=self.type, order=self.order)


class UInt8(SingleType, BigEndianMixin):
    '''Single byte unsigned integer (0 <= i <= 255).'''

    type = 'UNSIGNED CHAR'


class UInt32(SingleType, BigEndianMixin):
    '''4-byte (32bit) unsigned integer (0 <= i <= 4294967295)'''

    type = 'UNSIGNED INT'


class VarString(BaseType, BigEndianMixin):
    '''Unsigned 32-bit integer followed by array of octets
       which length is defined by the number.
    '''

    def __init__(self, value, order=None):

        BaseType.__init__(self)
        self.value = value
        if order is not None:
            self.order = order

    @classmethod
    def parseHead(cls, data, order=None):
        '''Parses data head and returns a pair of:
           parsed string and rest of the data.
        '''

        order = order or cls.order
        length, data = _parse_head(data, type='INT', order=order)
        if length == 0:  # empty string is a single \0 byte...
            dummy_byte, data = _parse_head(data, type='OCTET',
                    order=order)
        data_string, data = _parse_head(data, type='OCTET',
                times=length, order=order)
        return cls(data_string), data

    def code(self):
        '''Creates C structure of variable-length string `instance`
           as described in class docstring.
        '''

        length = len(self.value)
        length_code = _code(length, type='INT', order=self.order)
        fixed_string_code = _code(self.value, type='OCTET',
                times=length, order=self.order)
        return length_code + fixed_string_code


class AddressType(BaseType, BigEndianMixin):
    '''struct ADDRESS_T {
         uint32 length;
         octet[length] name;
         uint32 port;
       }
    '''

    def __init__(self, hostname, port, order=None):

        BaseType.__init__(self)
        self.hostname = hostname
        self.port = port
        if order is not None:
            self.order = order

    @classmethod
    def parseHead(cls, data, order=None):

        order = order or cls.order
        hostname, data = VarString.parseHead(data, order=order)
        port, data = UInt32.parseHead(data, order=order)
        return cls(hostname.value, port.value), data

    def code(self):

        port_parser = UInt32(self.port, order=self.order)
        return VarString(self.hostname).code() + port_parser.code()


class DataType(BaseType, BigEndianMixin):
    '''struct DATA_T {
         uint32 length;
         octet[length] text;
       }
    '''

    def __init__(self, text, order=None):

        BaseType.__init__(self)
        self.text = text
        if order is not None:
            self.order = order

    @classmethod
    def parseHead(cls, data, order=None):

        order = order or cls.order
        text, data = VarString.parseHead(data, order=order)
        return cls(text.value), data

    def code(self):

        text_parser = VarString(self.text, order=self.order)
        return text_parser.code()


class IdArrayType(BaseType, BigEndianMixin):
    '''struct ARRAY_ID_T {
         uint32 length;
         uint32[length] array;
       }
    '''

    def __init__(self, intlist, order=None):

        BaseType.__init__(self)
        self.intlist = intlist
        if order is not None:
            self.order = order

    @classmethod
    def parseHead(cls, data, order=None):

        order = order or cls.order
        length, data = UInt32.parseHead(data, order=order)
        intlist = list()
        for i in range(length.value):
            integer, data = UInt32.parseHead(data, order=order)
            intlist.append(integer.value)
        return cls(intlist), data

    def code(self):

        length = len(self.intlist)
        result_code = UInt32(length, order=self.order).code()
        for integer in self.intlist:
            result_code = result_code + \
                UInt32(integer, order=self.order).code()
        return result_code


class MessageAckType(BaseType, BigEndianMixin):
    '''struct ACKNOWLEDGEMENT_MSG_TYPE {
         uint8 message_id;
       }
    '''

    def __init__(self, message_id, order=None):

        BaseType.__init__(self)
        self.message_id = message_id
        if order is not None:
            self.order = order

    @classmethod
    def parseHead(cls, data, order=None):

        order = order or cls.order
        message_id, data = UInt8.parseHead(data, order=order)
        return cls(message_id.value), data

    def code(self):

        return UInt8(self.message_id, order=self.order).code()


class MessageAddressType(BaseType, BigEndianMixin):
    '''struct ADDRESS_MSG_T {
         uint8 message_id;
         ADDRESS_T address;
       }
    '''

    def __init__(self, message_id, address_object, order=None):

        BaseType.__init__(self)
        self.message_id = message_id
        self.address = address_object
        if order is not None:
            self.order = order

    @classmethod
    def parseHead(cls, data, order=None):

        order = order or cls.order
        message_id, data = UInt8.parseHead(data, order=order)
        address, data = AddressType.parseHead(data, order=order)
        return cls(message_id.value, address), data

    def code(self):

        return UInt8(self.message_id, order=self.order).code() + \
                self.address.code()


class MessageAddressesType(BaseType, BigEndianMixin):
    '''struct ADDRESSES_MSG_T {
         uint8 message_id;
         ADDRESS_T address1;
         ADDRESS_T address2;
       }
    '''

    def __init__(self, message_id, address1_object, address2_object,
            order=None):

        BaseType.__init__(self)
        self.message_id = message_id
        self.address1 = address1_object
        self.address2 = address2_object
        if order is not None:
            self.order = order

    @classmethod
    def parseHead(cls, data, order=None):

        order = order or cls.order
        message_id, data = UInt8.parseHead(data, order=order)
        address1_object, data = AddressType.parseHead(data, order=order)
        address2_object, data = AddressType.parseHead(data, order=order)
        return cls(message_id.value, address1_object, address2_object), data

    def code(self):

        return UInt8(self.message_id, order=self.order).code() + \
                self.address1.code() + self.address2.code()


class MessageInfoType(BaseType, BigEndianMixin):
    '''struct INFORMATION_MSG_T {
         uint8 message_id;
         ADDRESS_T address;
         DATA_T data;
       }
    '''

    def __init__(self, message_id, address_object, data_object, order=None):

        BaseType.__init__(self)
        self.message_id = message_id
        self.address = address_object
        self.data = data_object
        if order is not None:
            self.order = order

    @classmethod
    def parseHead(cls, data, order=None):

        order = order or cls.order
        message_id, data = UInt8.parseHead(data, order=order)
        address_object, data = AddressType.parseHead(data, order=order)
        data_object, data = DataType.parseHead(data, order=order)
        return cls(message_id.value, address_object, data_object), data

    def code(self):

        return UInt8(self.message_id, order=self.order).code() + \
                self.address.code() + self.data.code()


class MessageUserType(BaseType, BigEndianMixin):
    '''struct USER_MSG_T {
         uint8 message_id;
         ADDRESS_T address;
         DATA_T login;
         DATA_T password;
       }
    '''

    def __init__(self, message_id, address_object, login_object,
            password_object, order=None):

        BaseType.__init__(self)
        self.message_id = message_id
        self.address = address_object
        self.login = login_object
        self.password = password_object
        if order is not None:
            self.order = order

    @classmethod
    def parseHead(cls, data, order=None):

        order = order or cls.order
        message_id, data = UInt8.parseHead(data, order=order)
        address_object, data = AddressType.parseHead(data, order=order)
        login_object, data = DataType.parseHead(data, order=order)
        password_object, data = DataType.parseHead(data, order=order)
        return cls(message_id.value, address_object,
                login_object, password_object), data

    def code(self):

        return UInt8(self.message_id, order=self.order).code() + \
                self.address.code() + \
                self.login.code() + \
                self.password.code()


class MessageMailType(BaseType, BigEndianMixin):
    '''struct MAIL_MSG_T {
         uint8 message_id;
         ADDRESS_T address;
         uint32 mail_id;
         DATA_T recipient;
         DATA_T sender;
         DATA_T content;
       }
    '''

    def __init__(self, message_id, address_object, mail_id,
            recipient_object, sender_object, content_object, order=None):

        BaseType.__init__(self)
        self.message_id = message_id
        self.address = address_object
        self.mail_id = mail_id
        self.recipient = recipient_object
        self.sender = sender_object
        self.content = content_object
        if order is not None:
            self.order = order

    @classmethod
    def parseHead(cls, data, order=None):

        order = order or cls.order
        message_id, data = UInt8.parseHead(data, order=order)
        address_object, data = AddressType.parseHead(data, order=order)
        mail_id, data = UInt32.parseHead(data, order=order)
        recipient_object, data = DataType.parseHead(data, order=order)
        sender_object, data = DataType.parseHead(data, order=order)
        content_object, data = DataType.parseHead(data, order=order)
        return cls(message_id.value, address_object, mail_id.value, \
                recipient_object, sender_object, content_object), data

    def code(self):

        return UInt8(self.message_id, order=self.order).code() + \
                self.address.code() + \
                UInt32(self.mail_id, order=self.order).code() + \
                self.recipient.code() + \
                self.sender.code() + \
                self.content.code()


class MessageMailListType(BaseType, BigEndianMixin):
    '''struct LIST_MAIL_MSG_T {
         uint8 message_id;
         ADDRESS_T address;
         DATA_T recipient;
         ARRAY_ID_T messages;
       }
    '''

    def __init__(self, message_id, address_object, recipient_object,
            messages_object, order=None):

        BaseType.__init__(self)
        self.message_id = message_id
        self.address = address_object
        self.recipient = recipient_object
        self.messages = messages_object
        if order is not None:
            self.order = order

    @classmethod
    def parseHead(cls, data, order=None):

        order = order or cls.order
        message_id, data = UInt8.parseHead(data, order=order)
        address_object, data = AddressType.parseHead(data, order=order)
        recipient_object, data = DataType.parseHead(data, order=order)
        messages_object, data = IdArrayType.parseHead(data, order=order)
        return cls(message_id.value, address_object, recipient_object,
                messages_object), data

    def code(self):

        return UInt8(self.message_id, order=self.order).code() + \
                self.address.code() + \
                self.recipient.code() + \
                self.messages.code()
