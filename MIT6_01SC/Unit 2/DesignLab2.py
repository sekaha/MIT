from RobotSim import *

# Part 1
while True:
    refresh()
    tick()
    ac = Action(0,6)
    ac.execute()
    update_sim()