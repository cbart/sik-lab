''' Core Functionality of the server '''

from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading

from sklab.server.core.rpc_handler import *

class _RpcServerThread(threading.Thread):
    def __init__(self, rpc_server):
        super(_RpcServerThread, self).__init__()
        self._server = rpc_server
    def run(self):
        self._server.serve_forever()

def set_up(port, port2 = 1138):
    CoreService._inner_port = port
    CoreService._outer_port = port2
    CoreService._rpc_server = SimpleXMLRPCServer(("localhost", CoreService._inner_port))
    CoreService._rpc_server.register_function(rpc_connect,"core_service.connect")
    CoreService._rpc_server.register_function(rpc_disconnect,"core_service.disconnect")
    CoreService._rpc_server.register_function(rpc_isConnected,"core_service.isConnected")
    CoreService._rpc_server.register_function(rpc_signIn,"core_service.signIn")
    CoreService._rpc_server.register_function(rpc_signOut,"core_service.signOut")
    CoreService._rpc_server.register_function(rpc_isSignedIn,"core_service.isSignedIn")
    CoreService._rpc_server.register_function(rpc_setPort,"core_service.setPort")
    CoreService._rpc_server.register_function(rpc_getPort,"core_service.getPort")
    CoreService._rpc_server.register_function(rpc_registerUser,"core_service.registerUser")
    CoreService._rpc_server.register_function(rpc_send,"core_service.send")
    CoreService._rpc_server.register_function(rpc_receive,"core_service.receive")
    CoreService._rpc_server.register_function(rpc_shutdown,"core_service.shutdown")
    CoreService._rpc_server_thread = _RpcServerThread(CoreService._rpc_server)
    
def runRPCServer():
    CoreService._rpc_server_thread.start()

def runMain():
    pass


class CoreService(object):
    _inner_port = 4040
    _outer_port = 1138
    _rpc_server = None
    _rpc_server_thread = None