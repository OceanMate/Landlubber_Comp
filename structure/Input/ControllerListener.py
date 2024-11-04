# Docutmentation: https://www.pygame.org/docs/ref/joystick.html
import pygame

from dashboard.Dashboard import Dashboard

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
        
        if (pygame.joystick.get_count() != 0):
            self._connect_new_controller(0)

        
    def update (self):
        for event in pygame.event.get():
            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                self._connect_new_controller(event.device_index)

            if event.type == pygame.JOYDEVICEREMOVED:
                self.axis_state = {}
                self.is_button_down = {}
                self.dpad_state = {}
                print("Joystick disconnected")
                
                Dashboard().bottom_bar.update_controller_text("None")
            
            if event.type == pygame.JOYBUTTONDOWN:
                self.is_button_down[event.button] = True
            elif event.type == pygame.JOYBUTTONUP:
                self.is_button_down[event.button] = False
            elif event.type == pygame.JOYAXISMOTION:
                self.axis_state[event.axis] = event.value

            elif event.type == pygame.JOYHATMOTION:
                self.dpad_state[event.hat] = event.value

            
    def _connect_new_controller(self, id):
        # Initialize the first controller found
        self.joystick = pygame.joystick.Joystick(id)
        print(f"Controller connected: {self.joystick.get_name()}")
        
        # 
        self.is_button_down = {i: False for i in range(self.joystick.get_numbuttons())}
        self.axis_state = {i: 0.0 for i in range(self.joystick.get_numaxes())}
        self.dpad_state = {i: (0, 0) for i in range(self.joystick.get_numhats())}
        
        text = self.joystick.get_name()
        if (text == "Xbox One Controller"):
            text = "Xbox One"
        elif (text == "Controller (Gamepad F310)"):
            text = "Gamepad F310"
        elif (text == "Controller (XBOX 360 For Windows)"):
            text = "Xbox 360"
        
        Dashboard().bottom_bar.update_controller_text(controller_name=text)

    

    def get_button(self, button):
        if (pygame.joystick.get_count() == 0):
            return False
        return self.is_button_down[button]
    
    def get_axis(self, axis):
        if (pygame.joystick.get_count() == 0):
            return 0.0
        return self.axis_state[axis]

    def print_button(self, key):
        if key in self.is_button_down:
            print(f"Button {key}: {'Down' if self.is_button_down[key] else 'Up'}")
        else:
            print(f"Button {key} does not exist")
        
    def print_axis(self, key):
        print(f"Axis {key}: {self.axis_state[key]}")
