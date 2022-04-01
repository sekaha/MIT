import StateMachine as SM

class Accumulator(SM):
    def __init__(self,s0):
        self.start_state = s0

    def get_next_values(self,state,inp):
        return (state+inp,state+inp)