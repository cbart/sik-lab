''' Core Functionality of the server '''

from SimpleXMLRPCServer import SimpleXMLRPCServer

from sklab.server.core.rpc_handler import *

def set_up(port, port2 = 1138):
    CoreService._inner_port = port
    CoreService._outer_port = port2
    
def runRPCServer():
    CoreService._rpc_server = SimpleXMLRPCServer(("localhost", CoreService._inner_port))
    _server.register_function(rpc_connect,"core_service.connect")
    _server.register_function(rpc_disconnect,"core_service.disconnect")
    _server.register_function(rpc_isConnected,"core_service.isConnected")
    _server.register_function(rpc_signIn,"core_service.signIn")
    _server.register_function(rpc_signOut,"core_service.signOut")
    _server.register_function(rpc_isSignedIn,"core_service.isSignedIn")
    _server.register_function(rpc_setPort,"core_service.setPort")
    _server.register_function(rpc_getPort,"core_service.getPort")
    _server.register_function(rpc_registerUser,"core_service.registerUser")
    _server.register_function(rpc_send,"core_service.send")
    _server.register_function(rpc_receive,"core_service.receive")
    CoreService._rpc_server.serve_forever()

def runMain():
    pass


class CoreService(object):
    _inner_port = 4040
    _outer_port = 1138
    _rpc_server = None