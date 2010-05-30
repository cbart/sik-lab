# -*- coding: utf-8 -*-
'''Console frontend for P2P mail protocol client.
'''

import sys
import os.path
import getopt


__author__ = '''Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'''
__credits__ = ['''Cezary Bartoszuk''']


if __name__ == '__main__':
    sys.path.append(os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
        )
    )

from sklab.view import TermClient
from sklab.core import P2PController, RPCClient

def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
    except getopt.error as err:
        print "For help: use --help."
        sys.exit(2)

    if len(args) < 1:
        print "Please type in rpc port."
        sys.exit(3)
    elif len(args) > 1:
        print "Too manu arguments, only one expected."
        sys.exit(4)
    else:
        rpc_port = args[0]
        rpc_client = RPCClient('http://localhost:' + rpc_port)
        client = TermClient(P2PController(rpc_client))
        client.cmdloop()

if __name__ == '__main__':

    main()
