'''Core modules.'''


__maintainer__ = 'Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'
__credits__ = ['Cezary Bartoszuk']


class ControllerError(StandardError):

    pass


class P2PController:

    connection = None

    def assertNotConnected(self):

        if self.connection is not None:
            raise ControllerError("Already connected")

    def assertConnected(self):

        if self.connection is None:
            raise ControllerError("Not connected")

    def assertNotSignedIn(self):

        if self.userdata is not None:
            raise ControllerError("Already signed in")

    def assertSignedIn(self):

        if self.userdata is None:
            raise ControllerError("Not signed in")

    #TODO
    def connect(self, ip, port):

        self.connection = 1
