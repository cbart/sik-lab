''' Messages sent by network '''

from sklab.server.core.message_types import *
from sklab.server import state_machine
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
    
    def __init__(self, controller_object = state_machine, data_object = None):
        super(BaseMessage, self).__init__()
        self.controller = controller_object
        self.data = data_object
        
    def process(self):
        return self.controller.processMessage(self)
    
    def code(self):
        return self.data.code()
    
    def execute(self, state):
        raise NotImplementedError('`BaseMessage.execute` is abstract.')
    
    
class ConnectionRequestMessage(BaseMessage):
    
    data_cls = MessageAddressType
    msg_id = 1
    def execute(self, state):
        return state.handle_connectionRequestMessage(self)
        
class ConnectAckMessage(BaseMessage):
    
    data_cls = MessageAddressesType
    msg_id = 2
    def execute(self, state):
        return state.handle_connectAckMessage(self)

class DoesUserExistMessage(BaseMessage):
    
    data_cls = MessageUserType
    msg_id = 3
    def execute(self, state):
        return state.handle_doesUserExistMessage(self)

class UserExistsMessage(BaseMessage):
    
    data_cls = MessageUserType
    msg_id = 4
    def execute(self, state):
        return state.handle_userExistsMessage(self)
    
class IsUserActiveMessage(BaseMessage):
    
    data_cls = MessageInfoType
    msg_id = 5
    def execute(self, state):
        return state.handle_isUserActiveMessage(self)
    
class UserActiveMessage(BaseMessage):
    
    data_cls = MessageInfoType
    msg_id = 6
    def execute(self, state):
        return state.handle_userActiveMessage(self)
    
class MailSearchMessage(BaseMessage):
    
    data_cls = MessageMailListType
    msg_id = 7
    def execute(self, state):
        return state.handle_mailSearchMessage(self)
    
class MailMessage(BaseMessage):
    
    data_cls = MessageMailType
    msg_id = 8
    def execute(self, state):
        return state.handle_mailMessage(self)
    
class DamageSuccessorRequestMessage(BaseMessage):
    
    data_cls = MessageAddressesType
    msg_id = 9
    def execute(self, state):
        return state.handle_damageSuccessorRequestMessage(self)
    
class DamageSuccessorInfoMessage(BaseMessage):
    
    data_cls = MessageAddressType
    msg_id = 10
    def execute(self, state):
        return state.handle_damageSuccessorInfoMessage(self)
    
class DamageChangeSpareSuccessorMessage(BaseMessage):
    
    data_cls = MessageAddressesType
    msg_id = 11
    def execute(self, state):
        return state.handle_damageChangeSpareSuccessorMessage(self)

class DamageFixAckMessage(BaseMessage):
    
    data_cls = MessageAckType
    msg_id = 12
    def execute(self, state):
        return state.handle_damageFixAckMessage(self)
    
class ShutdownChangeSuccessorMessage(BaseMessage):
    
    data_cls = MessageAddressesType
    msg_id = 13
    def execute(self, state):
        return state.handle_shutdownChangeSuccessorMessage(self)
    
class ShutdownChangeSpareSuccessorMessage(BaseMessage):
    
    data_cls = MessageAddressesType
    msg_id = 14
    def execute(self, state):
        return state.handle_shutdownChangeSpareSuccessorMessage(self)
    
class ShutdownAckMessage(BaseMessage):

    data_cls = MessageAckType
    msg_id = 15
    def execute(self, state):
        return state.handle_shutdownAckMessage(self)
    
class NewSpareSuccessor(BaseMessage):
    
    data_cls = MessageAddressesType
    msg_id = 16
    def execute(self, state):
        return state.handle_newSpareSuccessor(self)