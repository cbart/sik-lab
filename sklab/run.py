# -*- coding: utf-8 -*-
'''Console frontend for P2P mail protocol client.
'''

import sys
import os.path


__author__ = '''Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'''
__credits__ = ['''Cezary Bartoszuk''']


if __name__ == '__main__':
    sys.path.append(os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
        )
    )


from sklab.view import TermClient
from sklab.core import P2PController


if __name__ == '__main__':

    client = TermClient(P2PController())
    client.cmdloop()

