from Debug import Debug
from transmission.ComsThread import ComsThread

class RobotState:
    _instance = None

    # When a new instance is created, sets it to the same global instance
    def __new__(cls):
        # If the instance is None, create a new instance
        # Otherwise, return already created instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._start()
        return cls._instance
    
    def _start(self):
        self._teleop_enabled = False
        self._teleop_to_be_initialized = False
        self._disabled_to_be_initialized = False
        
    def should_init_teleop(self):
        should_boot_teleop = self._teleop_enabled and self._teleop_to_be_initialized
        self._teleop_to_be_initialized = False
        
        return should_boot_teleop
    
    def should_init_disable(self):
        should_boot_disable = not self._teleop_enabled and self._disabled_to_be_initialized
        self._disabled_to_be_initialized = False
        
        return should_boot_disable
    
    def is_teleop_enabled(self):
        return self._teleop_enabled
    
    def enable_teleop(self):
        # prevent enabling teleop if not connected to pi, disable if debugging
        if not Debug.ignoreComsToEnable and not ComsThread().connected:
            print("Cannot enable teleop, not connected to pi")
            return False
        
        
        ComsThread().set_enabled(True)
        self._teleop_enabled = True
        self._teleop_to_be_initialized = True
        return True
    
    def disable_robot(self):
        ComsThread().set_enabled(False)
        
        self._teleop_enabled = False
        self._disabled_to_be_initialized = True