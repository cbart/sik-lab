''' state machine '''

from sklab.server.state_machine.states import *

_current_state = OfflineState()

def processMessage(msg):
    _current_state.handle_message(msg)
    
def changeState(newState):
    _current_state.exit()
    _current_state = newState
    _current_state.enter()