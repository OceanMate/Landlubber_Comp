from structure.Input.KeyboardListener import KeyboardListener
from structure.commands.InputScheduler import InputScheduler

class KeyboardInput(InputScheduler):
    def __init__(self, key: str):
        KeyboardListener().add_key(key)
        super().__init__(lambda: KeyboardListener().is_key_down(key))

    
    
   
        