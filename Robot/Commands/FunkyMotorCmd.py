from structure.commands.Command import Command
from Robot.Subsystems.LinearMotors import LinearMotors

class FunkyMotorCmd(Command):
    def __init__(self, linear_motors):
        super().__init__()
        self.linear_motors = linear_motors
        super().add_requirement(self.linear_motors)

    
    def initalize(self):
        print("Funky fresh linear motors are running")

        self.linear_motors.runMotors(1, 1, 1)
    
    def execute(self):
        return
    
    def end(self, interrupted):
        if (interrupted):
            print("Funky command interrupted")
        self.linear_motors.runMotors(0, 0, 0)
    
    def is_finished(self):
        return False