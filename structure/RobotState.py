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
        
    def is_init_teleop(self):
        should_boot_teleop = self._teleop_enabled and self._teleop_to_be_initialized
        self._teleop_to_be_initialized = False
        
        return should_boot_teleop
    
    def is_init_disable(self):
        should_boot_disable = not self._teleop_enabled and self._disabled_to_be_initialized
        self._disabled_to_be_initialized = False
        
        return should_boot_disable
    
    def is_teleop_enabled(self):
        return self._teleop_enabled
    
    def enable_teleop(self):
        self._teleop_enabled = True
        self._teleop_to_be_initialized = True
    
    def disable_robot(self):
        self._teleop_enabled = False
        self._disabled_to_be_initialized = True