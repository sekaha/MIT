"""
    all state machines share these few common abilities:
    start, step, and transduce

    a transducer is defined by the following:

    a set of inputs, a set of outputs, and a set of states
    a next state function, n(i,s) -> s+
    an output function, o(i,s) -> o+
    an initial state s0

"""

class StateMachine:
    start_state = None
    def __init__(self):
        self.state = 0

    # requires a start_state to be initialized
    def start(self):
        # takes no input
        self.state = self.start_state

    def step(self, inp):
        s, o = self.get_next_values(self.state,inp)
        self.state = s
        return o

    def transduce(self,inputs):
        self.start()
        return [self.step(inp) for inp in inputs]

    # takes the state at time t and the input at time t as input,
    # and returns the state at time t + 1 and the output at time t
    def get_next_values(self,state,inp):
        # does not mutate the state variable, must not have side effects, this is a pure function
        pass