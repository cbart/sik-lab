from sklab.server.core import CoreService

def rpc_connect(ip, port):
    return {'result': false}

def rpc_disconnect():
    return {'result': false}

def rpc_isConnected():
    return {'result': false}

def rpc_signIn(login, password):
    return {'result': false}

def rpc_signOut():
    return {'result': false}

def rpc_isSignedIn():
    return {'result': false}

def rpc_setPort(port):
    return {'result': false}

def rpc_getPort():
    return {'result': CoreService._outer_port}

def rpc_registerUser(login, password):
    return {'result': false}

def rpc_send(login, content):
    return {'result': false}

def rpc_receive():
    return {'result': []}
