# Docutmentation: https://www.pygame.org/docs/ref/joystick.html
import pygame

''' Xbox 360 Controller Mapping
Left Stick:
Left -> Right   - Axis 0
Up   -> Down    - Axis 1

Right Stick:
Left -> Right   - Axis 3
Up   -> Down    - Axis 4

Left Trigger:
Out -> In       - Axis 2

Right Trigger:
Out -> In       - Axis 5

Buttons:
A Button        - Button 0
B Button        - Button 1
X Button        - Button 2
Y Button        - Button 3
Left Bumper     - Button 4
Right Bumper    - Button 5
Back Button     - Button 6
Start Button    - Button 7
L. Stick In     - Button 8
R. Stick In     - Button 9
Guide Button    - Button 10

Hat/D-pad:
Down -> Up      - Y Axis
Left -> Right   - X Axis
'''

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
        else:
            self._connect_new_controller(0)
        
        self.is_button_down = {}
        self.axis_state = {}
        self.dpad_state = {}
        
        
        
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
            
            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                self._connect_new_controller(event.instance_id)
                print(f"Joystick {self.joystick.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                del self.joystick
                print(f"Joystick {event.instance_id} disconnected")
            
    def _connect_new_controller(self, id):
        # Initialize the first controller found
        self.joystick = pygame.joystick.Joystick(id)
        print(f"Controller connected: {self.joystick.get_name()}")
        self.is_button_down = {i: False for i in range(self.joystick.get_numbuttons())}
        self.axis_state = {i: 0.0 for i in range(self.joystick.get_numaxes())}
    

    def get_button(self, button):
        if (pygame.joystick.get_count() == 0):
            return False
        return self.is_button_down[button]
    
    def get_axis(self, axis):
        if (pygame.joystick.get_count() == 0):
            return 0.0
        return self.axis_state[axis]

    def print_button(self, key):
        print( f"Button {key}: {'Down' if self.is_button_down[key] else 'Up'}")
        
    def print_axis(self, key):
        print(f"Axis {key}: {self.axis_state[key]}")
    