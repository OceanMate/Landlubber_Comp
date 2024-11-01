from structure.Input.KeyboardListener import KeyboardListener
from structure.Input.InputScheduler import InputScheduler

class KeyboardInput(InputScheduler):
    def __init__(self, key: str):
        # Adds the key to the KeyboardListener to listen to
        KeyboardListener().add_key(key)
        
        # Sets up the InputScheduler with a lambda function that checks if the key is pressed
        # Using the lambda function allows for dynamic checking of the key state (will update as the key state changes)
        super().__init__(lambda: KeyboardListener().is_key_down(key))
