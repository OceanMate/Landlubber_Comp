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
        yaw_speed = 0
        # add a big deadband since another rotation control is on on the other axis
        if abs(self.zRotation()) > 0.25:
            yaw_speed = self.zRotation()
        
        # xSpeed, ySpeed, and zRotation are all from -1 to 1
        self.linear_motors.run_motors(self.xSpeed() * 0.5, 
                                      self.ySpeed() * 0.5, 
                                      yaw_speed * 0.33 )
    
    def end(self, interrupted):
        self.linear_motors.stop_motors()
    
    def is_finished(self):
        return False