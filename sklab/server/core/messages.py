''' Messages sent by network '''

from sklab.server.core.message_types import *
import inspect


def getClassForMsgId(id):
    mod = __import__('sklab.server.core.messages')
    mod = getattr(mod, 'server')
    mod = getattr(mod, 'core')
    mod = getattr(mod, 'messages')
    # FIXME
    for obj in dir(mod):
        obj  = getattr(mod, obj)
        if inspect.isclass(obj):
            if 'msg_id' in obj.__dict__ and \
                id == getattr(obj, 'msg_id'):
                return obj
    return None

class BaseMessage(object):
    
    msg_id = 0
    
    def __init__(self, controller_object, data_object = None):
        super(BaseMessage, self).__init__()
        self.controller = controller_object
        self.data = data_object
        
    def process(self, *args, **kwargs):
        raise NotImplementedError('`BaseMessage.process` is abstract.')
    
    def code(self):
        return self.data.code()
    
    
class ConnectionRequestMessage(BaseMessage):
    
    data_cls = MessageAddressType
    msg_id = 1
        
class ConnectAckMessage(BaseMessage):
    
    data_cls = MessageAddressesType
    msg_id = 2

class DoesUserExistMessage(BaseMessage):
    
    data_cls = MessageUserType
    msg_id = 3

class UserExistsMessage(BaseMessage):
    
    data_cls = MessageUserType
    msg_id = 4
    
class IsUserActiveMessage(BaseMessage):
    
    data_cls = MessageInfoType
    msg_id = 5
    
class UserActiveMessage(BaseMessage):
    
    data_cls = MessageInfoType
    msg_id = 6
    
class MailSearchMessage(BaseMessage):
    
    data_cls = MessageMailListType
    msg_id = 7
    
class MailMessage(BaseMessage):
    
    data_cls = MessageMailType
    msg_id = 8
    
class DamageSuccessorRequestMessage(BaseMessage):
    
    data_cls = MessageAddressesType
    msg_id = 9
    
class DamageSuccessorInfoMessage(BaseMessage):
    
    data_cls = MessageAddressType
    msg_id = 10
    
class DamageChangeSpareSuccessorMessage(BaseMessage):
    
    data_cls = MessageAddressesType
    msg_id = 11

class DamageFixAckMessage(BaseMessage):
    
    data_cls = MessageAckType
    msg_id = 12
    
class ShutdownChangeSuccessorMessage(BaseMessage):
    
    data_cls = MessageAddressesType
    msg_id = 13
    
class ShutdownChangeSpareSuccessorMessage(BaseMessage):
    
    data_cls = MessageAddressesType
    msg_id = 14
    
class ShutdownAckMessage(BaseMessage):

    data_cls = MessageAckType
    msg_id = 15
    
class NewSpareSuccessor(BaseMessage):
    
    data_cls = MessageAddressesType
    msg_id = 16