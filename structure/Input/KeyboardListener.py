# use the command to use this library: pip install pynput
from pynput import keyboard
from queue import Queue

class KeyboardListener:
    _instance = None

    # When a new instance is created, sets it to the same global instance
    def __new__(cls):
        # If the instance is None, create a new instance
        # Otherwise, return already created instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._start()
        return cls._instance        
        
    # Private method that acts as an initializer
    def _start (self):
        self.is_keys_down = {}
        self.pressQueue = Queue()
        self.releaseQueue = Queue()
        
        # Start the listener (a thread) to start listening for key presses
        # steals your password nerd
        self.listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        self.listener.start()
    
    def stop_listener(self):
        self.listener.stop()
    
    # add a key to check on 
    def add_key(self, key: str):
        
        self.is_keys_down[key] = False

    def update (self):
        
        # Check for new pressed keys from the thread
        while not self.pressQueue.empty():
            pressed_key = self.pressQueue.get()
            self.is_keys_down[pressed_key] = True
                            
        # Check for new released keys from the thread
        while not self.releaseQueue.empty():
            released_key = self.releaseQueue.get()
            self.is_keys_down[released_key] = False
                    
    # Private methods to handle key press and release events
    def _on_press(self, key):
        try:
            self.pressQueue.put(key.char)
        except AttributeError:
            special_key = str(key)
            special_key = special_key.replace("Key.", "")
            self.pressQueue.put(special_key)

    def _on_release(self, key):
        try:
            self.releaseQueue.put(key.char)
        except AttributeError:
            special_key = str(key)
            special_key = special_key.replace("Key.", "")
            self.releaseQueue.put(special_key)

    # Print the current state of the keys, used for debugging   
    def printKeys (self):
        for key, value in self.is_keys_down.items():
            print(f"{key}: {value}")
                
    # Check if a key is currently pressed down
    def is_key_down(self, key: str):
        if key not in self.is_keys_down.keys():
            self.add_key(key)
        
        return self.is_keys_down.get(key, False)