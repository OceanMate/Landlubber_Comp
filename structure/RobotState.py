class RobotState:
    def __init__(self):
        self.enabled = False
        self.teleop_to_be_initialized = False
        self.disabled_to_be_initialized = False
    
    def set_enabled(self, enabled):
        self.enabled = enabled
    
    def is_enabled(self):
        return self.enabled
    
    def set_teleop_to_be_initialized(self, teleop_to_be_initialized):
        self.teleop_to_be_initialized = teleop_to_be_initialized
    
    def is_teleop_to_be_initialized(self):
        return self.teleop_to_be_initialized    
    
    def set_disabled_to_be_initialized(self, disabled_to_be_initialized):
        self.disabled_to_be_initialized = disabled_to_be_initialized
    
    def is_disabled_to_be_initialized(self):
        return self.disabled_to_be_initialized