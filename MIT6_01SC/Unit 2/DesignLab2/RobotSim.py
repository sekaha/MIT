# Design Lab 3: All Carrot, No Stick (PDF)
# So like, this requires a robot, which I don't have
# therefore I shall be using my LED package to generate some graphics
from LED import *
import StateMachine 
from random import randint
from math import cos, sin, radians, ceil, floor, pi

set_orientation(1)
set_fps(30)

CELL_SIZE = 2

class Robot():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.angle = randint(0,360)
        offset_angle = (180/7)
        self.sensors = [Ray(offset*offset_angle-90) for offset in range(0,8)]
        self.sonars = [sensor.update_distance(self.x,self.y,self.angle) for sensor in self.sensors]
        self.trail = False
        self.max_spd = 1
        self.max_rot_spd = 15

    def get_sonars(self):
        return self.sonars

    def move(self,fvel,rvel):
        fvel = max(-self.max_spd,min(self.max_spd,fvel))
        #rvel = max(-self.max_rot_spd,min(self.max_rot_spd,rvel))
        self.angle += rvel
        direction = radians(self.angle)

        target_x = self.x + cos(direction)*fvel
        target_y = self.y + sin(direction)*fvel

        #if (world[floor(target_y)][floor(target_x)] == 0):
        self.x = target_x
        self.y = target_y

    def draw_self(self):
        x2 = self.x + cos(radians(self.angle))*5
        y2 = self.y + sin(radians(self.angle))*5

        for num, sensor in enumerate(self.sensors):
            self.sonars[num] = sensor.update_distance(self.x,self.y,self.angle)

        #draw_rectangle(self.x*CELL_SIZE,self.y*CELL_SIZE,CELL_SIZE,CELL_SIZE,CYAN)
        draw_point(self.x*CELL_SIZE,self.y*CELL_SIZE,CYAN)
        if (self.trail):
            self.make_trail()

    def make_trail(self):
        set_canvas(decal_layer)
        draw_point(self.x*CELL_SIZE,self.y*CELL_SIZE,color_hsv((self.angle/360)*255,255,127))
        reset_canvas()

class Ray():
    def __init__(self,angle_offset):
        self.angle_offset = angle_offset

    def scan(self,x,y,dir):
        max_dist = 100
        angle = radians(dir)
        target_x, target_y = x, y
        accuracy = 1

        for cell in range(max_dist):
            try:
                if (world[floor((target_y))][floor((target_x))] == 1):
                    if accuracy == 1:
                        target_x -= cos(angle)*accuracy
                        target_y -= sin(angle)*accuracy
                        accuracy = 0.01
                    else:
                        return target_x, target_y
            except:
                return target_x, target_y
            
            if accuracy == 1:
                set_alpha(128)
                draw_point(target_x*CELL_SIZE,target_y*CELL_SIZE,color_hsv(self.angle_offset+cell*2,255,255))
                set_alpha(255)
            else:
                draw_point(target_x*CELL_SIZE,target_y*CELL_SIZE,RED)
            target_x += cos(angle)*accuracy
            target_y += sin(angle)*accuracy
        return target_x, target_y

    def update_distance(self,x,y,angle):
        x2, y2 = self.scan(x,y,angle+self.angle_offset)

        # typical distance formula
        return (((x-x2)**2+(y-y2)**2)**0.5)

    
class Action:
    def __init__(self,fvel=0.0,rvel=0.0):
        self.fvel = fvel
        self.rvel = rvel

    def execute(self):
        robot.move(self.fvel,self.rvel)

    def __str__(self):
        return f"fvel = {self.fvel}, rvel = {self.rvel}"

def enable_trail():
    robot.trail = True

def draw_level():
    for y, column in enumerate(world):
        for x, cell in enumerate(column):
            if (cell == 1):
                draw_rectangle(x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE,CELL_SIZE,GREY)

"""def make_decal_layer():
    global decal_layer
    decal_layer = create_canvas(get_width_adjusted(),get_height_adjusted())
    set_canvas(decal_layer)
    draw_level()
    reset_canvas()"""

def update_sim():
    tick()
    refresh()
    draw_canvas(0,0,decal_layer)
    robot.draw_self()
    draw_level()
    draw()

decal_layer = create_canvas(get_width_adjusted(),get_height_adjusted())

# game object set up
world = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [ 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

robot = Robot(12,12) #Robot(2,2) #