from structure.Command import Command

class DefaultLinearMotorCmd(Command):
    def __init__(self, linear_motors):
        super().__init__()
        self.linear_motors = linear_motors
    
    def initalize(self):
        # xSpeed, ySpeed, and zRotation are all from -1 to 1
        self.linear_motors.runMotors(1, 1, 1)

    
    def execute(self):
        print("Running linear motors")

        return
    
    def end(self, interrupted):
        self.linear_motors.runMotors(0, 0, 0)
    
    def is_finished(self):
        return False