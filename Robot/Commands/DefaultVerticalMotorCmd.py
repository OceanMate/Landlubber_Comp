from structure.commands.Command import Command

class DefaultVerticalMotorCmd(Command):
    def __init__(self, vertical_motors, speed):
        super().__init__()
        self.vertical_motors = vertical_motors
        super().add_requirement(self.vertical_motors)
        
        self.speed = speed
    
    def initalize(self):
        return
    
    def execute(self):
        # speed is from -1 to 1
        self.vertical_motors.run_motors(self.speed())
    
    def end(self, interrupted):
        self.vertical_motors.stop_motors()
    
    def is_finished(self):
        return False