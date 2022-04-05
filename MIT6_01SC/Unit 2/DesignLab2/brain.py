from asyncio.constants import SENDFILE_FALLBACK_READBUFFER_SIZE
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

"""When there is nothing nearby, it should move straight forward.
2. As soon as it reaches an obstacle in front, it should follow the boundary
of the obstacle, keeping the right side of the robot between 0.3 and 0.5
meters from the obstacle"""

class part_2(StateMachine):
    start_state = "search"
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

        if (state == "search"):
            if (front_distance > (self.desired+0.1)):
                return "search", Action(front_distance-self.desired,0)
            else:
                # if left ray needs evened out
                if sonars[3] > sonars[4]:
                    return "even_left", Action(0,1)
                else:
                    return "even_right", Action(0,-1)
                
        elif (state == "even_right"):
            if approx_equal(sonars[3],sonars[4],0.1):
                    return "rotate_left", Action(0,0)
            else:
                return "even_right", Action(0,1)
                
        elif (state == "even_left"):
            if approx_equal(sonars[3],sonars[4],0.01):
                    return "rotate_left", Action(0,0)
            else:
                return "even_right", Action(0,1)
        elif (state == "rotate_left"):
            return "follow", Action(0,-90)
        elif (state == "align"):
            if (sonars[6] > 0) and (sonars[6] < (self.desired+1)):
                print(sonars[7], self.desired+1, (sonars[6] < (self.desired)))
                ratio = (sonars[7]/sonars[6])-cos(pi/7)

                if ratio > 0:
                    return "align_left", Action(0,1)
                elif ratio < 0:
                    return "align_right", Action(0,-1)
                else:
                    return "follow", Action(0,0)
            else:
                return "rotate_right", Action(0,0)
        elif (state == "align_right"):
            ratio = (sonars[7]/sonars[6])-cos(pi/7)
            if abs(ratio) > 0.01:
                return "align_right", Action(0,1)
            else: return "follow", Action(0,0)
        elif (state == "align_left"):
            ratio = (sonars[7]/sonars[6])-cos(pi/7)
            if abs(ratio) > 0.01:
                return "align_left", Action(0,-1)
            else:
                return "follow", Action(0,0)
        elif (state == "follow"):
            if (sonars[3] < 1 or sonars[4] < 1):
                front_distance = (self.desired+1)

            if (front_distance > (self.desired+0.1)):
                return "align", Action(front_distance-self.desired,0)
            else:
                # if left ray needs evened out
                if (sonars[3] - sonars[4]) > 0.1:
                    return "even_left", Action(front_distance-self.desired,1)
                elif (sonars[3] - sonars[4]) < -0.1:
                    return "even_right", Action(front_distance-self.desired,-1)
                else:
                    return "rotate_left", Action(front_distance-self.desired,0)
        elif (state == "rotate_right"):
            return "search", Action(0,90)
        else:
            return "h", Action(0,0)

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