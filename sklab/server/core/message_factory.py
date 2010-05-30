''' Factory for messages. '''

from sklab.server.core import messages
from sklab.server.core import CoreService
from sklab.server.core.message_types import UInt8

def createMessagesFromString(raw_string):
    result_msgs = []
    while raw_string:
        msg_id, raw_string = UInt8.parseHead(raw_string)
        msg_id = msg_id.value
        raw_string = repr(msg_id) + raw_string
        msg_cls = messages.getClassForMsgId(msg_id)
        data_object, raw_string = msg_cls.data_cls.parseHead(raw_string)
        result_msgs.append(msg_cls(CoreService, data_object))
    return result_msgs

def createMessagesFromSocket(socket):
    pass