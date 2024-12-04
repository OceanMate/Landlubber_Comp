from structure.commands.Command import Command
from Robot.Subsystems.LinearMotors import LinearMotors

class DefaultLinearMotorCmd(Command):
    def __init__(self, linear_motors):
        super().__init__()
        self.linear_motors = linear_motors
        super().add_requirement(self.linear_motors)
    
    
    def initalize(self):
        print("Running linear motors")

        # xSpeed, ySpeed, and zRotation are all from -1 to 1
        self.linear_motors.runMotors(1, 0, 0)
    
    def execute(self):
        return
    
    def end(self, interrupted):
        if (interrupted):
            print("Default command interrupted")
        self.linear_motors.stop_motors()
    
    def is_finished(self):
        return False