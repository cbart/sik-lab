'''Core modules.'''


__maintainer__ = 'Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'
__credits__ = ['Cezary Bartoszuk']


class ControllerError(StandardError):

    pass


class P2PController:

    def assertNotConnected(self):

        if self.connection is not None:
            raise ControllerError("Already connected")

    def connect(self, ip, port):

        pass
