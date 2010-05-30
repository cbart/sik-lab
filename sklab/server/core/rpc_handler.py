from sklab.server.core import CoreService

from sklab.server.core.messages import BaseMessage
from sklab.server import state_machine

class RPCBaseMessage(BaseMessage):
    def __init__(self, controller_object = state_machine):
        super(BaseMessage, self).__init__(controller_object)
    def code(self):
        raise NotImplementedError('`RPCBaseMessage.code` is not available.')

class ConnectRPC(RPCBaseMessage):
    def __init__(self, ip, port, controller_object = state_machine):
        super(BaseMessage, self).__init__(controller_object)
        self.ip = ip
        self.port = port
    def execute(self, state):
        return state.handle_rpc_connect(self)

class DisonnectRPC(RPCBaseMessage):
    def execute(self, state):
        return state.handle_rpc_disconnect(self)
    
class IsConnectedRPC(RPCBaseMessage):
    def execute(self, state):
        return state.handle_rpc_isConnected(self)
    
class SignInRPC(RPCBaseMessage):
    def __init__(self, login, password, controller_object = state_machine):
        super(BaseMessage, self).__init__(controller_object)
        self.login = login
        self.password = password
    def execute(self, state):
        return state.handle_rpc_signIn(self)
    
class SignOutRPC(RPCBaseMessage):
    def execute(self, state):
        return state.handle_rpc_signOut(self)
    
class IsSignedInRPC(RPCBaseMessage):
    def execute(self, state):
        return state.handle_rpc_isSignedIn(self)

class SetPortRPC(RPCBaseMessage):
    def __init__(self, port, controller_object = state_machine):
        super(BaseMessage, self).__init__(controller_object)
        self.port = port
    def execute(self, state):
        return state.handle_rpc_setPort(self)

class GetPortRPC(RPCBaseMessage):
    def execute(self, state):
        return state.handle_rpc_getPort(self)

class RegisterUserRPC(RPCBaseMessage):
    def __init__(self, login, password, controller_object = state_machine):
        super(BaseMessage, self).__init__(controller_object)
        self.login = login
        self.password = password
    def execute(self, state):
        return state.handle_rpc_registerUser(self)

class SendRPC(RPCBaseMessage):
    def __init__(self, login, content, controller_object = state_machine):
        super(BaseMessage, self).__init__(controller_object)
        self.login = login
        self.content = content
    def execute(self, state):
        return state.handle_rpc_send(self)

class ReceiveRPC(RPCBaseMessage):
    def execute(self, state):
        return state.handle_rpc_receive(self)

class ShutdownRPC(RPCBaseMessage):
    def execute(self, state):
        return state.handle_rpc_shutdown(self)

def rpc_connect(ip, port):
    msg = ConnectRPC(ip, port)
    result = msg.process()
    return {'result': False}

def rpc_disconnect():
    msg = DisonnectRPC()
    result = msg.process()
    return {'result': False}

def rpc_isConnected():
    msg = IsConnectedRPC()
    result = msg.process()
    return {'result': False}

def rpc_signIn(login, password):
    msg = SignInRPC(login, password)
    result = msg.process()
    return {'result': False}

def rpc_signOut():
    msg = SignOutRPC()
    result = msg.process()
    return {'result': False}

def rpc_isSignedIn():
    msg = IsSignedIn()
    result = msg.process()
    return {'result': False}

def rpc_setPort(port):
    msg = SetPortRPC(port)
    result = msg.process()
    return {'result': False}

def rpc_getPort():
    msg = GetPortRPC()
    result = msg.process()
    return {'result': CoreService._outer_port}

def rpc_registerUser(login, password):
    msg = RegisterUserRPC(login, password)
    result = msg.process()
    return {'result': False}

def rpc_send(login, content):
    msg = SendRPC(login, content)
    result = msg.process()
    return {'result': False}

def rpc_receive():
    msg = ReceiveRPC()
    result = msg.process()
    return {'result': []}

def rpc_shutdown():
    msg = ShutdownRPC()
    result = msg.process()
#    CoreService._rpc_server.shutdown()
#    CoreService._rpc_server_thread.join()
    return {'result': True}
