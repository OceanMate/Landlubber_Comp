from structure.commands.Command import Command

class DefaultVerticalMotorCmd(Command):
    def __init__(self, vertical_motors, left_trigger, right_trigger):
        super().__init__()
        self.vertical_motors = vertical_motors
        super().add_requirement(self.vertical_motors)
        
        self.left_trigger = left_trigger  # function to get left trigger value (from 0 to 1)
        self.right_trigger = right_trigger # function to get right trigger value (from 0 to 1)
        
    
    def initalize(self):
        return
    
    def execute(self):
        speed = self.right_trigger() - self.left_trigger()
        
        # speed is from -1 to 1
        self.vertical_motors.run_motors(speed)
    
    def end(self, interrupted):
        self.vertical_motors.stop_motors()
    
    def is_finished(self):
        return False