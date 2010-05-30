from sklab.server.core import CoreService

def rpc_connect(ip, port):
    return {'result': False}

def rpc_disconnect():
    return {'result': False}

def rpc_isConnected():
    return {'result': False}

def rpc_signIn(login, password):
    return {'result': False}

def rpc_signOut():
    return {'result': False}

def rpc_isSignedIn():
    return {'result': False}

def rpc_setPort(port):
    return {'result': False}

def rpc_getPort():
    return {'result': CoreService._outer_port}

def rpc_registerUser(login, password):
    return {'result': False}

def rpc_send(login, content):
    return {'result': False}

def rpc_receive():
    return {'result': []}

def rpc_shutdown():
    CoreService._rpc_server.shutdown()
    CoreService._rpc_server_thread.join()
    return {'result': True}
