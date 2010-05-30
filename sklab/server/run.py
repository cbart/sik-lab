''' run server process '''

import sys

import sklab.server.core

def runCoreService(port, port2=1138):
    core.set_up(port, port2)
    core.runRPCServer()
    core.runMain()

if __name__ == '__main__':
    runCoreService(sys.argv[1])