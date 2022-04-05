from RobotSim import *
from StateMachine import *
from math import cos, pi, degrees, copysign, acos

def approx_equal(f1 : float, f2 : float, epsilon : float):
    return (abs(f1-f2) < epsilon)

class part_1(StateMachine):
    startState = "initialize"
    desired = 2.0

    # intakes sensory info, that is, the robot's sonars
    # outputs an action and state
    def get_next_values(self, state, inp):
        distance = (inp.get_sonars()[3] + inp.get_sonars()[4]) / 2
        return (state, Action(distance-self.desired, 0))


class part_2(StateMachine):
    start_state = "init"
    desired = 2.0

    # intakes sensory info, that is, the robot's sonars
    # outputs an action and state
    def get_next_values(self, state, inp):
        sonars = inp.get_sonars()
        #print(' '.join([f"{sonar:.2f}" for sonar in sonars]))
        if (sonars[3] == 0 or sonars[4] == 0):
            front_distance = 0
        else:
            front_distance = (sonars[3] + sonars[4]) / 2
            
        right_distance = (sonars[7])
        left_distance  = (sonars[0])
        
        # see if ratio is um = right ratio :)

        # move approach if nothing nearby
        print(state)
        if (state == "init"):
            if (front_distance > self.desired):
                    new_state = "approach"
            else:
                new_state = "align"
                
            return new_state, Action(0, 0)

        if (state == "approach"):
            new_state = state

            # love comparing floats, this is best solution
            if ((front_distance-self.desired) < 0.01) \
                or sonars[3] < 0.01 or sonars[4] < 0.01:
                new_state = "align"
            return new_state, Action(front_distance-self.desired,0)

        elif (state == "follow"):
            new_state = "align_right"

            # love comparing floats, this is best solution
            if ((front_distance-self.desired) < 0.01) \
                or sonars[3] < 0.01 or sonars[4] < 0.01:
                new_state = "align"
            
            return new_state, Action(front_distance-self.desired,0)

        elif (state == "align"):
            aligned = (sonars[3] - sonars[4])
            
            #print(aligned, approx_equal(aligned, 0, 0.01), approx_equal(front_distance, self.desired, 0.05))
            if approx_equal(aligned, 0, 0.01):
                if (approx_equal(front_distance, self.desired, 0.05)):
                    return "align_right", Action(0, -90)
                else:
                    return "approach", Action(0, -1)
            else:90
                return "align", Action(0, -1)
            #else:    
            #    return "align",  Action(0, degrees())
        elif (state == "align_right"):
            if any(sonar==0 for sonar in sonars):
                print("in wall")
                return "align", Action(0,0)
            else:
                 # using a right triangle to deterime if we're perfectly parallel to the wall
                right_ratio = sonars[7]/sonars[6]
                diff = right_ratio - cos(pi/7)
                if (abs(diff) > 0.05):
                    return "follow", Action(0,22.5) #11.25
                else:
                    print("right is aligned")
                    if front_distance < self.desired:
                        return "follow", Action(0, -22.5)
                    else:
                        return "follow", Action(0,0)

        else:
            return state, Action(0,0)

def step():
    action = sm.step(robot)
    action.execute()

sm = part_2()
sm.start()

# Part 1
while True:
    step()
    enable_trail()
    update_sim()
    