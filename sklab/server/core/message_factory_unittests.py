''' Unittests for message_factory and messages'''

import unittest

from sklab.server.core.messages import *
from sklab.server.core.message_factory import *
from sklab.server.core.message_types import *

class TestFactory(unittest.TestCase):
    def testGettingClassForMsgId(self):
        msg_id = 0
        self.assertEqual(getClassForMsgId(msg_id), BaseMessage)
        msg_id = 5
        self.assertEqual(getClassForMsgId(msg_id), IsUserActiveMessage)
        msg_id = 20
        self.assertEqual(getClassForMsgId(msg_id), None)
    def testFactoryFromString(self):
        data_object = MessageAddressType(ConnectionRequestMessage.msg_id, AddressType('localhost', 8080))
        data_str = data_object.code()
        msg_list = createMessagesFromString(data_str)
        self.assertEqual(len(msg_list), 1)
        msg = msg_list[0]
        self.assertEqual(msg.msg_id, ConnectionRequestMessage.msg_id)
        

if __name__ == '__main__':
    unittest.main()