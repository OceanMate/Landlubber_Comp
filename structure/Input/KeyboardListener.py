# use the command to use this library: pip install pynput
from pynput import keyboard
from queue import Queue

# a data class to hold key information
class Key:
    key_name: str
    down: bool

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
        
    
    def _start (self):
        self.keys = []
        self.pressQueue = Queue()
        self.releaseQueue = Queue()
        
        # Start the listener (a thread) to start listening for key presses
        # steals your password nerd
        listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        listener.start()
    
    def stop_listener(self):
        keyboard.Listener.stop()
    
    # add a key to check on 
    def add_key(self, key: str):
        key_obj = Key()
        key_obj.key_name = key
        key_obj.down = False
        
        self.keys.append(key_obj)

    def update (self):
        
        # Check for new pressed keys from the thread
        while not self.pressQueue.empty():
            pressed_key = self.pressQueue.get()
            for stored_key in self.keys:
                if stored_key.key_name == pressed_key:
                    
                    stored_key.down = True
        
        # Check for new released keys from the thread
        while not self.releaseQueue.empty():
            released_key = self.releaseQueue.get()
            for stored_key in self.keys:
                if stored_key.key_name == released_key:
                    stored_key.down = False
                    
    
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
        #print(len(self.keys))
        for stored_key in self.keys:
            print(f"Key: {stored_key.key_name}, Down: {stored_key.down}")
    
    def is_key_down(self, key: str):
        for stored_key in self.keys:
            if stored_key.key_name == key:
                return stored_key.down
        return None



