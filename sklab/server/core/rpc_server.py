# -*- coding: utf-8 -*-

import threading
from SimpleXMLRPCServer import \
        SimpleXMLRPCServer


class RPCServerThread(threading.Thread):

    def __init__(self, rpc_server):

        super(RPCServerThread, self).__init__()
        self.rpc_server = rpc_server

    def run(self):

        self.rpc_server.serve_forever()

    def stop(self):

        self.rpc_server.shutdown()


class RPCServer(object):

    def __init__(self, host, port, rpc_instance):

        super(RPCServer, self).__init__()
        self.rpc_instance = rpc_instance
        self.host = host
        self.port = port

    def _createRPCServer(self):

        return SimpleXMLRPCServer((self.host, self.port), allow_none=True)

    def run(self):

        self.rpc_server = self._createRPCServer()
        self.rpc_server.register_instance(self.rpc_instance,
                allow_dotted_names=False)
        self.rpc_thread = RPCServerThread(self.rpc_server)
        self.rpc_thread.start()

    def stop(self):

        self.rpc_thread.stop()
        self.rpc_thread.join(10)

