# -*- coding: utf-8 -*-
'''Module responsible for terminal user interface.'''

import cmd

from sklab.view.commands import \
        ConnCommand, argument_extractor
from sklab.view.util import \
        error_handler
from sklab.core.config import Config

__maintainer__ = 'Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'
__credits__ = ['Cezary Bartoszuk']


_TERM_PS = '> '


class TermClient(cmd.Cmd):
    '''Terminal P2P Mail client.'''

    prompt = _TERM_PS

    def __init__(self, client_controller, *args, **kwargs):
        '''Creates ``CmdClient`` object which corresponds with given
           client_controller.
        '''

        cmd.Cmd.__init__(self, *args, **kwargs)
        self.controller = client_controller

    def _error(self, message):
        '''Manages printing error information.'''

        print "Error:", message


    @error_handler
    @argument_extractor
    def do_conn(self, ip, port=Config.defaul_port):
        '''Usage: conn ip [port]
             ip - IPv4 address (ex. 192.168.1.1)
             port - the other client's listening port
        '''
        command = ConnCommand()
        print "IP: ", ip, "; Port: ", port
        #self.client.connect(**command.output_args)

    def do_EOF(self, line):
        return True
