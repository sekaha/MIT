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

# This is often just called R
# It is an important primitive in a compositional system of linear time-invariant systems
class Delay(StateMachine):
    def __init__(self,initial_state):
        self.start_state = initial_state

    def get_next_values(self, state, inp):
        return (inp,state)

# Cascade composition
class Cascade(StateMachine):
    def __init__(self,sm1,sm2):
        self.m1 = sm1
        self.m2 = sm2
        self.start_state = sm1.start_state

    def get_next_values(self, state, inp):
        s1, o1 = self.m1.get_next_values(state,inp)
        s2, o2 = self.m2.get_next_values(s1,o1)
        return (s2,o2)

# Parallel composition
class Parallel(StateMachine):
    def __init__(self,sm1,sm2):
        self.m1 = sm1
        self.m2 = sm2
        self.start_state = (sm1.start_state,sm2.start_state)

    def get_next_values(self, state, inp):
        (s1,s2) = state
        (new_s1, o1) = self.m1.get_next_values(s1,inp)
        (new_s2, o2) = self.m2.get_next_values(s2,inp)
        return ((new_s1,new_s2),(o1,o2))

class PureFunction(StateMachine):
    def __init__(self,f):
        # should be a function that we can use
        self.f = f

    def get_next_values(self, state, inp):
        return (state,self.f(inp))

# output is its input,,, not sure why this is useful but ay, it's part of specifications
class Wire(StateMachine):
    def get_next_values(self, state, inp):
        return (state,inp)

# another why does this exist module haha
class Constant(StateMachine):
    def __init__(self,initial_state):
        self.start_state = initial_state

    def get_next_values(self, state, inp):
        return (state,self.start_state)