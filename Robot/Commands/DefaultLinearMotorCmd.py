from structure.commands.Command import Command

class DefaultLinearMotorCmd(Command):
    def __init__(self, linear_motors, xSpeed, ySpeed, zRotation, slow_button):
        super().__init__()
        self.linear_motors = linear_motors
        super().add_requirement(self.linear_motors)
        
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.zRotation = zRotation
        self.slow_button = slow_button # function to get slow button value (True or False)
    
    def initalize(self):
        return 
    
    def execute(self):
        slow_speed = 0
        if self.slow_button():
            slow_speed = 0.5
        else:
            slow_speed = 1

        # xSpeed, ySpeed, and zRotation are all from -1 to 1
        self.linear_motors.run_motors(self.xSpeed() * slow_speed, 
                                      self.ySpeed() * slow_speed, 
                                      self.zRotation() * 0.33 * slow_speed)
    
    def end(self, interrupted):
        self.linear_motors.stop_motors()
    
    def is_finished(self):
        return False