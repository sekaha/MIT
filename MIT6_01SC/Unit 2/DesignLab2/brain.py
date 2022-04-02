from RobotSim import *
from StateMachine import *


class part_1(StateMachine):
    startState = "initialize"
    desired = 2.0

    # intakes sensory info, that is, the robot's sonars
    # outputs an action and state
    def get_next_values(self, state, inp):
        distance = (inp.get_sonars()[3] + inp.get_sonars()[4]) / 2
        return (state, Action(distance-self.desired, 0))

def step():
    (state, action) = sm.get_next_values(0,robot)
    action.execute()

class part_2(StateMachine):
    startState = "initialize"
    desired = 2.0

    # intakes sensory info, that is, the robot's sonars
    # outputs an action and state
    def get_next_values(self, state, inp):
        front_distance = (inp.get_sonars()[3])
        # move forward if nothing nearby
        if (front_distance > self.desired):
            return (state, Action(0.1))
        else:
            # if distance on right side is big enough, continue to move
            return (state, Action(0, 1))

def step():
    (state, action) = sm.get_next_values(0,robot)
    action.execute()

sm = part_1()

# Part 1
while True:
    step()
    enable_trail()
    update_sim()