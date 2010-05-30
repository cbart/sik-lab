''' Defining states for state machine '''

class BaseState(object):
    def exit(self):
        pass
    def enter(self):
        pass
    def handle_message(self, msg):
        return msg.execute(self)
    def handle_rpc_connect(self, msg):
        pass
    def handle_rpc_disconnect(self, msg):
        pass
    def handle_rpc_isConnected(self, msg):
        pass
    def handle_rpc_signIn(self, msg):
        pass
    def handle_rpc_signOut(self, msg):
        pass
    def handle_rpc_isSignedIn(self, msg):
        pass
    def handle_rpc_setPort(self, msg):
        pass
    def handle_rpc_getPort(self, msg):
        pass
    def handle_rpc_registerUser(self, msg):
        pass
    def handle_rpc_send(self, msg):
        pass
    def handle_rpc_receive(self, msg):
        pass
    def handle_rpc_shutdown(self, msg):
        pass
    def handle_connectionRequestMessage(self, msg):
        pass
    def handle_connectAckMessage(self, msg):
        pass
    def handle_doesUserExistMessage(self, msg):
        pass
    def handle_userExistsMessage(self, msg):
        pass
    def handle_isUserActiveMessage(self, msg):
        pass
    def handle_userActiveMessage(self, msg):
        pass
    def handle_mailSearchMessage(self, msg):
        pass
    def handle_mailMessage(self, msg):
        pass
    def handle_damageSuccessorRequestMessage(self, msg):
        pass
    def handle_damageSuccessorInfoMessage(self, msg):
        pass
    def handle_damageChangeSpareSuccessorMessage(self, msg):
        pass
    def handle_damageFixAckMessage(self, msg):
        pass
    def handle_shutdownChangeSuccessorMessage(self, msg):
        pass
    def handle_shutdownChangeSpareSuccessorMessage(self, msg):
        pass
    def handle_shutdownAckMessage(self, msg):
        pass
    def handle_newSpareSuccessor(self, msg):
        pass

    
class OfflineState(BaseState):
    pass
