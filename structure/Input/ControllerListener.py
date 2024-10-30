import pygame
import sys

class ControllerListener:
    _instance = None

    # When a new instance is created, sets it to the same global instance
    def __new__(cls):
        # If the instance is None, create a new instance
        # Otherwise, return already created instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._start()
        return cls._instance   

    def _start (self):
        #initializes pygame and joystick
        pygame.init()
        pygame.joystick.init()
        
        #Checks if controller is connected
        if pygame.joystick.get_count() == 0:
            print("No controller detected.")
            sys.exit()
            
        # Initialize the first controller found
        self.joystick = pygame.joystick.Joystick(0)
        
        print(f"Controller connected: {self.joystick.get_name()}")
        
        self.is_button_down = {}
        self.axis_state = {}
        self.dpad_state = {}
        
        self.is_button_down = {i: False for i in range(self.joystick.get_numbuttons())}
        self.axis_state = {i: 0.0 for i in range(self.joystick.get_numaxes())}
        
    def update (self):
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                self.is_button_down[event.button] = True
            elif event.type == pygame.JOYBUTTONUP:
                self.is_button_down[event.button] = False
            elif event.type == pygame.JOYAXISMOTION:
                self.axis_state[event.axis] = event.value

            elif event.type == pygame.JOYHATMOTION:
                self.dpad_state[event.hat] = event.value

    def get_button(self, button):
        return self.is_button_down[button]
    
    def get_axis(self, axis):
        return self.axis_state[axis]

    def print_button(self, key):
        print( f"Button {key}: {'Down' if self.is_button_down[key] else 'Up'}")
        
    def print_axis(self, key):
        print(f"Axis {key}: {self.axis_state[key]}")
    