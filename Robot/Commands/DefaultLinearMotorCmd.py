from structure.commands.Command import Command

class DefaultLinearMotorCmd(Command):
    def __init__(self, linear_motors, xSpeed, ySpeed, left_trigger, right_trigger):
        super().__init__()
        self.linear_motors = linear_motors
        super().add_requirement(self.linear_motors)
        
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.left_trigger = left_trigger
        self.right_trigger = right_trigger
    
    def initalize(self):
        return 
    
    def execute(self):
        zRotation = 0
        if self.right_trigger() > 0.5:
            zRotation = 1
        elif self.left_trigger() > 0.5:
            zRotation = -1
        
        # xSpeed, ySpeed, and zRotation are all from -1 to 1
        self.linear_motors.runMotors(self.xSpeed(), self.ySpeed(), zRotation)
    
    def end(self, interrupted):
        self.linear_motors.stop_motors()
    
    def is_finished(self):
        return False