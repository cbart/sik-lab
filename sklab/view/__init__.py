# -*- coding: utf-8 -*-
'''Module responsible for terminal user interface.'''

import cmd

from sklab.view.commands import *
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

        print "SKLAB terminal. Type Ctrl-D to exit."

    def _error(self, message):
        '''Manages printing error information.'''

        print "Error:", message

    @error_handler
    @argument_extractor
    def do_conn(self, ip, port=Config.default_port):
        '''Connects to the network

           Usage: conn ip [--port=port]
             ip - IPv4 address (ex. 192.168.1.1)
             port - the other client's listening port (defaults to 1138)
        '''
        command = ConnCommand(self.controller)
        command.execute(ip, port)

    @error_handler
    @argument_extractor
    def do_in(self, login, password):
        '''Signs in into the network.

           Usage: in login password
             login - name of the user used to logon
             password - user's password
        '''
        command = SignInCommand(self.controller)
        command.execute(login, password)

    @error_handler
    @argument_extractor
    def do_out(self):
        '''Signs out of the network.

           Usage: out
        '''
        command = SignOutCommand(self.controller)
        command.execute()

    @error_handler
    @argument_extractor
    def do_send(self, login, content):
        '''Sends message to user identified with `login`.

           Usage: send login content
             login - name of the addressee
             content - message content
        '''
        command = SendCommand(self.controller)
        command.execute(login, content)

    @error_handler
    @argument_extractor
    def do_pop(self):
        '''Calls the network for messages.

           Usage: pop
        '''
        command = ReceiveCommand(self.controller)
        command.execute()

    @error_handler
    @argument_extractor
    def do_register(self, login, password,
            ip=Config.self_ip, port=Config.default_port):
        '''Tries to register a user in the network.

           Usage: register login password [--ip=ip ] [--port=port]
             login - name of the user which we want to register
             password - passwort we would like to have
             ip - ip address of the network node we would like to register in
               (defaults to 127.0.0.1)
             port - node's listening port (defaults to 1138)
        '''
        command = RegisterUserCommand(self.controller)
        command.execute(login, password, ip, port)

    def do_EOF(self, line):
        '''Quits the terminal.

           Usage: Ctrl-D
        '''
        command = ExitCommand(self.controller)
        command.execute()

        return True
