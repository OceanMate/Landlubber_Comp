from structure.commands.Command import Command

class DefaultVerticalMotorCmd(Command):
    def __init__(self, vertical_motors, left_trigger, right_trigger, slow_button):
        super().__init__()
        self.vertical_motors = vertical_motors
        super().add_requirement(self.vertical_motors)
        
        self.left_trigger = left_trigger  # function to get left trigger value (from 0 to 1)
        self.right_trigger = right_trigger # function to get right trigger value (from 0 to 1)
        self.slow_button = slow_button # function to get slow button value (True or False)
    
    def initalize(self):
        return
    
    def execute(self):
        slow_speed = 1
        if self.slow_button():
            slow_speed = 0.5
        else:
            slow_speed = 1
            
        right_speed = 0
        if self.right_trigger() > 0.75:
            right_speed = 1
        elif self.right_trigger() > 0:
            right_speed = 0.5

        
        left_speed = 0
        if self.left_trigger() > 0.75:
            left_speed = 1
        elif self.left_trigger() > 0:
            left_speed = 0.5

        
        speed = (left_speed - right_speed) * slow_speed
        
        # speed is from -1 to 1
        self.vertical_motors.run_motors(speed)
    
    def end(self, interrupted):
        self.vertical_motors.stop_motors()
    
    def is_finished(self):
        return False