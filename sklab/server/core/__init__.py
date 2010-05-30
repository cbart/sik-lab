''' Core Functionality of the server '''

def runMainThread():
    pass

class CoreService(object):
    _DEF_POLL_TIMEOUT = 5000
    _MSG_ACK_TIMEOUT = 10000
    _inner_port = 4040
    _outer_port = 1138
    _rpc_server = None
    _rpc_server_thread = None
    mails_map = {} #login - [MailMessage...] 
    known_users = {} #login - MessageUserType
    successor = None # MessageUserType
    spare_successor = None # MessageUserType
    buffer = [] #[BaseMessage...]
