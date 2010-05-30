''' run server process '''

import sys

import sklab.server.core as core_service

def runCoreService(port, port2=1138):
    core_service.set_up(port, port2)
    core_service.runRPCServer()
    core_service.runMain()

if __name__ == '__main__':
    runCoreService(sys.argv[1])