''' Core Functionality of the server '''

def runMainThread():
    pass

class CoreService(object):
    _inner_port = 4040
    _outer_port = 1138
    _rpc_server = None
    _rpc_server_thread = None