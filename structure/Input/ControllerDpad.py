from structure.Input.ControllerListener import ControllerListener
from structure.Input.ControllerListener import DpadDirection
from structure.Input.InputScheduler import InputScheduler

class ControllerDpad(InputScheduler):
    def __init__(self, dpad_enum: DpadDirection):
        
        # Sets up the InputScheduler with a lambda function that checks if the button is pressed
        # Using the lambda function allows for dynamic checking of the button state (will update as the button state changes)
        super().__init__(lambda: ControllerListener().get_dpad() == dpad_enum)    