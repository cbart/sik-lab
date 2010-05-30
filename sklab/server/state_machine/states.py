''' Defining states for state machine '''

from sklab.server.state_machine import *

class BaseState(object):
    def exit(self):
        pass
    def enter(self):
        pass
    def handle_message(self, msg):
        return msg.execute(self)
    def handle_rpc_connect(self, msg):
        raise IllegalStateException(self)
    def handle_rpc_disconnect(self, msg):
        raise IllegalStateException(self)
    def handle_rpc_isConnected(self, msg):
        raise IllegalStateException(self)
    def handle_rpc_signIn(self, msg):
        raise IllegalStateException(self)
    def handle_rpc_signOut(self, msg):
        raise IllegalStateException(self)
    def handle_rpc_isSignedIn(self, msg):
        raise IllegalStateException(self)
    def handle_rpc_setPort(self, msg):
        raise IllegalStateException(self)
    def handle_rpc_getPort(self, msg):
        raise IllegalStateException(self)
    def handle_rpc_registerUser(self, msg):
        raise IllegalStateException(self)
    def handle_rpc_send(self, msg):
        raise IllegalStateException(self)
    def handle_rpc_receive(self, msg):
        raise IllegalStateException(self)
    def handle_rpc_shutdown(self, msg):
        raise IllegalStateException(self)
    def handle_connectionRequestMessage(self, msg):
        raise IllegalStateException(self)
    def handle_connectAckMessage(self, msg):
        raise IllegalStateException(self)
    def handle_doesUserExistMessage(self, msg):
        raise IllegalStateException(self)
    def handle_userExistsMessage(self, msg):
        raise IllegalStateException(self)
    def handle_isUserActiveMessage(self, msg):
        raise IllegalStateException(self)
    def handle_userActiveMessage(self, msg):
        raise IllegalStateException(self)
    def handle_mailSearchMessage(self, msg):
        raise IllegalStateException(self)
    def handle_mailMessage(self, msg):
        raise IllegalStateException(self)
    def handle_damageSuccessorRequestMessage(self, msg):
        raise IllegalStateException(self)
    def handle_damageSuccessorInfoMessage(self, msg):
        raise IllegalStateException(self)
    def handle_damageChangeSpareSuccessorMessage(self, msg):
        raise IllegalStateException(self)
    def handle_damageFixAckMessage(self, msg):
        raise IllegalStateException(self)
    def handle_shutdownChangeSuccessorMessage(self, msg):
        raise IllegalStateException(self)
    def handle_shutdownChangeSpareSuccessorMessage(self, msg):
        raise IllegalStateException(self)
    def handle_shutdownAckMessage(self, msg):
        raise IllegalStateException(self)
    def handle_newSpareSuccessor(self, msg):
        raise IllegalStateException(self)

class OfflineState(BaseState):
    pass
