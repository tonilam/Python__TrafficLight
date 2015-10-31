#-----Statement of Authorship----------------------------------------#
#
#  By submitting this task the signatories below agree that it
#  represents our own work and that we both contributed equally to
#  it.  We are aware of the University rule that a student must not
#  act in a manner which constitutes academic dishonesty as stated
#  and explained in QUT's Manual of Policies and Procedures,
#  Section C/5.3 "Academic Integrity" and Section E/2.1 "Student
#  Code of Conduct".
#
#  Driver's student no: N9516778
#  Driver's name: LAM KWOK SHING (TONI)
#
#  Navigator's student no: N8938521
#  Navigator's name: HUAMING WEI (BRIAN) 
#--------------------------------------------------------------------#


#-----Task Description-----------------------------------------------#
#
#  TRAFFIC LIGHT
#
#  In this task you will create a simple simulation using the PyGame
#  package.  The program will simulate a stream of cars passing a
#  traffic light.  Each time the user clicks the mouse in the window
#  the traffic light should change colour in the usual green-yellow-
#  red-green cycle.  When the light is red the cars should stop
#  once they reach it or a stationary car in front.  Otherwise cars
#  should keep entering the flow at one end of the screen and
#  exiting at the other.  More details, including a tutorial on
#  PyGame programming, can be found in the instruction sheet.
#--------------------------------------------------------------------#


#-----Students' Solution---------------------------------------------#
#
#  Complete the task by filling in the template below.

import pygame

#### PUT YOUR SOLUTION HERE

#
#--------------------------------------------------------------------#
import sys
from random import randint
import time

## Program Configuration
#--------------------------------------------------------------------#

# Initialize constant
# -- Window -- #
WINDOW_CONFIG = {
    "caption"           :'Trafic light',
    "width"             :900,
    "height"            :600,
    "background_color"  :(255, 255, 255)
    }

# -- Trafic light -- #
TRAFICLIGHT_CONFIG = {
    "image"   : {
        "green"     :'.\Images\green.png',
        "yellow"    :'.\Images\yellow.png',
        "red"       :'.\Images\\red.png'
        },
    "init_light"    :"green",
    "x_cord"        :800,
    "y_cord"        :45,
    "yellowlight_duration":500
    }

# -- Car -- #
CAR_CONFIG = {
    "image_prefix"  :'.\Images\car',
    "image_ext"     :'.png',
    "width"         :300,
    "height"        :300,
    "color_index_min"   :0,
    "color_index_max"   :4,
    "speed"         :2
    }

# -- Road -- #
ROAD_CONFIG = {
    "line_amount"   :4,
    "max_car_no"    :5,
    "x_cord"        :50,
    "distance_from_traficlight" :10,
    "height"        :100,
    "road_color"    :(0, 0, 0),
    "line_color"    :(255, 255, 255),
    "dashed_line" : {
        "length"    :200,
        "start_x"   :50,
        "thickness" :10,
        "amount"    :4
        },
    "safety_distance" :10,
    "new_car_probability" :1.1   # percentage from 0 to 100
    }

# -- Animate -- #
ANIMATE_CONFIG = {
    "delay" :0.005   # in second
    }

## Class defination.
#--------------------------------------------------------------------#
class Scene:

    # initialize object.
    # Return: void
    def __init__(self, window_config, road_config, traficlight_config):
        self.config = window_config
        self.road_start_y_cord = traficlight_config["y_cord"]*2\
                                 +road_config["distance_from_traficlight"]
        self.window = pygame.display.set_mode((self.config["width"],
                                               self.config["height"]))
        self.window.fill(self.config["background_color"])
        self.road_height = road_config["height"]
        self.road_color = road_config["road_color"]
        self.no_of_lines = road_config["line_amount"]
        self.line_width = road_config["height"]
        self.line_color = road_config["line_color"]
        self.dashed_line = road_config["dashed_line"]
        self.stop_line_start_x_pos = traficlight_config["x_cord"]
        pygame.display.set_caption(self.config["caption"])

    # A function to get the width of the scene.
    # Return: void
    def get_width(self):
        return self.config["width"]
    
    # A function to draw the road on the scene.
    # Return: void
    def draw_road(self):
        # draw the black road.
        road_starting_x_pos = 0
        road_starting_y_pos = self.road_start_y_cord
        road_width = self.config["width"]
        road_height = self.line_width * self.no_of_lines
        road_area = road_starting_x_pos, road_starting_y_pos,\
                    road_width, road_height
        pygame.draw.rect(self.window, self.road_color, road_area)

        # draw the dashed seperation lines.
        for row in range(1,self.no_of_lines):
            for col in range(self.dashed_line["amount"]):
                
                start_x_pos = col*self.dashed_line["length"]+\
                    self.dashed_line["start_x"]
                dashed_line = start_x_pos,\
                    self.road_height+self.line_width*row- \
                    self.dashed_line["thickness"]/2, \
                    (road_width-self.stop_line_start_x_pos)/ \
                    (self.dashed_line["amount"]/2),\
                    self.dashed_line["thickness"]
                pygame.draw.rect(self.window, self.line_color, dashed_line)
        stop_line = self.stop_line_start_x_pos,\
                    self.road_height,\
                    self.dashed_line["thickness"],\
                    self.line_width*self.dashed_line["amount"]
        pygame.draw.rect(self.window, self.line_color, stop_line)

    # A function to update a specific image and its position on the scene.
    # Return: void
    def update_instance(self, image, position):
        self.window.blit(image, position)

    # end of class: Scene

class MouseEvent:

    # initialize object.
    # Return: void
    def __init__(self, light_config):
        self.traficlight_color = light_config["init_light"]
        self.event = pygame.event
        self.yellow_light_duration = light_config["yellowlight_duration"]
        self.yellowlight_counter = 0
        self.terminated = False

    # A function to check if the user terminated the program.
    # Return: Boolean
    def is_terminated(self):
        return self.terminated

    # A function to set the current light color.
    # Return: void
    def set_light(self, light):
        self.traficlight_color = light
        
    # A function to get the update light color in case the listener
    # has change it.
    # Return: String
    def get_current_light(self):
        return self.traficlight_color

    # A function to listen to user's mouse action and change.
    # the trafic light status accordingly
    # Return: void
    def listen(self):
        # Part 1 - Handling yellow light condition.
        # Check if the light is yellow, then change the counter and
        # if the duration is passed, then change the light to red
        if self.traficlight_color == "yellow":
            if self.yellowlight_counter < self.yellow_light_duration:
                self.yellowlight_counter += 1
            else:
                self.traficlight_color = "red"

        # Part 2 - Handling (a) green and red light conditions and
        #                   (b) quit the program.
        # Listen for mouse event and change the status,
        # or change the termination status if the user quit the program.
        for event in self.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.traficlight_color == "green":
                    self.traficlight_color = "yellow"
                    self.yellowlight_counter = 0
                elif self.traficlight_color == "red":
                    self.traficlight_color = "green"
            elif event.type == pygame.QUIT:
                self.terminated = True
                
    # end of class: MouseEvent
    
class TraficLight:

    # initialize object.
    # Return: void
    def __init__(self, light_config):
        # Load the trafic light images
        self.image_options = {}
        for key in light_config["image"].keys():
            self.image_options[key]=\
                pygame.image.load(light_config["image"][key]).convert()
        self.set_status( light_config["init_light"] )

        # set attributes
        self.position = self.image_options[self.status].get_rect(
                            center = (light_config["x_cord"],
                                      light_config["y_cord"])
                        )
        self.yellowlight_duration = light_config["yellowlight_duration"]
    

    # A function to set the status of the trafic light and change its image
    # that corresponding to the status
    # Return: void
    def set_status(self, light):
        self.status = light
        self.image = self.image_options[light]

    # A function to get the trafic light current image
    # Return: image object
    def load_img(self):
        return self.image

    # A function to get the trafic light yellow light duration
    # Return: Integer
    def getYellowLightDuration(self):
        return self.yellowlight_duration

    # A function to get the trafic light current status
    # Return: String
    def get_status(self):
        return self.status
    
    # A function to get the trafic light current position
    # Return: Rectangle object
    def get_pos(self):
        return self.position
    
    # A function to get the trafic light current x-coordination
    # Return: Integer
    def get_x_pos(self):
        return self.position.centerx

    # end of class: TraficLight
        
class Car:

    # initialize object.
    # Return: void
    def __init__(self, car_id, line_index, car_config, road_config):
        self.config = car_config
        self.car_id = car_id
        self.line = line_index
        self.safety_distance = road_config["safety_distance"]
        self.repaint()
        self.position = self.car.get_rect(
                center = (car_config["width"],
                          road_config["x_cord"]+road_config["height"]*\
                          (line_index+1)
                          )
            )
        self.reset_pos()

    # A function to get the car image.
    # Return: image object
    def load_img(self):
        return self.car

    # A function to get the current position of this car
    # Return: Rectangle object
    def get_pos(self):
        return self.position

    # A function to get the current position of this car
    # Return: Rectangle object
    def get_x_pos(self):
        return self.position.left

    # A function to reset a car to the starting point
    # Return:  void
    def reset_pos(self):
        self.position.right = 0

    # A function to repaint the car with a new random image.
    # Return: void
    def repaint(self):
        car_color_code = str(randint(self.config["color_index_min"],
                                     self.config["color_index_max"]))
        self.car_image = self.config["image_prefix"] + car_color_code +\
                         self.config["image_ext"]
        self.car = pygame.image.load(self.car_image).convert_alpha()

    # A function to move the car if possible.
    # Return: True if the car can move forward
    #         False if the car cannot move anymore
    def can_move(self, cars_on_the_road):
        if (traficlight.get_status() == "red")\
            and\
            (self.position.right == traficlight.get_x_pos()):
            return False
        car_index = cars_on_the_road[self.line].index(self.car_id)
        # if there is some cars in the front,
        # than check whether it is safe to move forward
        if (car_index > 0) and\
           (self.position.right + self.safety_distance\
            >= cars[self.line][cars_on_the_road[self.line][car_index-1]].\
               get_x_pos()):
            return False
        return True

    # A method that try to move the car forward, reset the position
    # if cannot move
    #
    # Return:
    # True meaning that the car is keep running on the road
    # False meaning that the car cannot move any further
    def forward(self, cars_on_the_road, max_width):
        # if the condition is good to move forward, then move its position
        if  self.can_move(cars_on_the_road):
            velocity = [self.config["speed"], 0]
            self.position = self.position.move(velocity)
        # if the position is out of bound, then reset the position
        if self.position.left > max_width:
            self.reset_pos() 
            return False
        return True
   
    # end of class: Car

class Road:

    # initialize object.
    # Return: void
    def __init__(self, road_config, scene):
        self.config = road_config
        self.scene = scene
        self.max_width = scene.get_width()
        self.cars_on_the_road = self.empty_car_list_on_the_road()

    # A function to create an empty car list that will record
    # which car is being running on the road.
    # Return: list
    def empty_car_list_on_the_road(self):
        cars_list = []
        for line_no in range(self.config["line_amount"]):
            cars_list.append([])
        return cars_list

    # A function to create a car randomly
    # Return: void
    def random_create_car(self, cars, line):
        # Check whether the road still have capicity to add car
        if len(self.cars_on_the_road[line]) < self.config["max_car_no"]:
            if len(self.cars_on_the_road[line]) == 0:
                new_car_id = 0
            else:
                new_car_id = self.cars_on_the_road[line][-1] + 1
            # if the random number is inside the probability, then
            # start to create car and put it on the road
            if (randint(1,100) < self.config["new_car_probability"] ):
                # if the new id is out of range, then move the index back to 0
                if new_car_id >= self.config["max_car_no"]:
                    new_car_id = 0
                # repaint the car before putting it on the road
                cars[line][new_car_id].repaint()
                self.cars_on_the_road[line].append(new_car_id)

    # A function to randomly create a car for every line of the road if
    # the road is not full and move every car forward if possible.
    # Return: void
    def update_trafic(self, cars):
        for line in range(self.config["line_amount"]):
            self.random_create_car(cars, line)

            # For each car on the same line of the road, try to move it forward.
            # If it can move, then update the instance in the scene;
            # otherwise, remove it from the list.
            for runningcar_id in self.cars_on_the_road[line]:
                if cars[line][runningcar_id].forward(
                        self.cars_on_the_road,self.max_width):
                    self.scene.update_instance(
                        cars[line][runningcar_id].load_img(),
                        cars[line][runningcar_id].get_pos()
                    )
                else:
                    self.cars_on_the_road[line].remove(runningcar_id)

    # End of class: Road
        
## Functions defination
#--------------------------------------------------------------------#

# A function to create an empty car list for the required amount of lines.
# Return: list
def empty_car_list_for_each_line(line_amount):
    temp_car_list = []
    for line_no in range(line_amount):
        temp_car_list.append([])
    return temp_car_list

# A function to create a full cars list that possible to run on the road.
# Return: list
def create_car_objects(car_config, road_config):
    car_list = empty_car_list_for_each_line(road_config["line_amount"])
    for line_index in range(road_config["line_amount"]):
        for car_index in range(road_config["max_car_no"]):
            new_car = Car(car_index, line_index, car_config, road_config)
            car_list[line_index].append( new_car )
    return car_list
    
## Main program goes from here
#--------------------------------------------------------------------#
pygame.init()

# create the essential objects
scene = Scene(WINDOW_CONFIG, ROAD_CONFIG, TRAFICLIGHT_CONFIG)
traficlight = TraficLight(TRAFICLIGHT_CONFIG)
mouse_listener = MouseEvent(TRAFICLIGHT_CONFIG)
road = Road(ROAD_CONFIG, scene)

# create the car list and initialize all cars into the list
cars = create_car_objects(CAR_CONFIG, ROAD_CONFIG)

# looping the processes and take action based on user action
while not mouse_listener.is_terminated():
    
    # listen to user interaction and change the trafic light
    mouse_listener.set_light(traficlight.get_status())
    mouse_listener.listen()
    traficlight.set_status(mouse_listener.get_current_light())

    # re-draw the basic instants of the scene
    scene.draw_road()

    # show the trafic light with current status
    scene.update_instance(traficlight.load_img(), traficlight.get_pos())

    # Update all cars position and status
    road.update_trafic(cars)

    # display the frame and slow down the program
    pygame.display.flip()
    time.sleep(ANIMATE_CONFIG["delay"])

pygame.quit()
        
# End of program.
