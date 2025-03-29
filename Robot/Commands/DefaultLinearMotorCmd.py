from structure.commands.Command import Command

class DefaultLinearMotorCmd(Command):
    def __init__(self, linear_motors, xSpeed, ySpeed, zRotation):
        super().__init__()
        self.linear_motors = linear_motors
        super().add_requirement(self.linear_motors)
        
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.zRotation = zRotation
    
    def initalize(self):
        return 
    
    def execute(self):
        # xSpeed, ySpeed, and zRotation are all from -1 to 1
        self.linear_motors.run_motors(self.xSpeed(), self.ySpeed(), self.zRotation())
    
    def end(self, interrupted):
        self.linear_motors.stop_motors()
    
    def is_finished(self):
        return False