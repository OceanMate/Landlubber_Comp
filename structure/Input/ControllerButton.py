from structure.Input.ControllerListener import ControllerListener
from structure.Input.InputScheduler import InputScheduler

class ControllerButton(InputScheduler):
    def __init__(self, button: int):
        
        # Sets up the InputScheduler with a lambda function that checks if the button is pressed
        # Using the lambda function allows for dynamic checking of the button state (will update as the button state changes)
        super().__init__(lambda: ControllerListener().get_button(button))    