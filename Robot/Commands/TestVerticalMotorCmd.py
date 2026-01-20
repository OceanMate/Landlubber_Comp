from structure.commands.Command import Command
from Robot.Subsystems.VerticalMotors import VerticalMotors

class TestVerticalMotorCmd(Command):
    def __init__(self, vertical_motors : VerticalMotors, left_bumper, right_bumper):
        super().__init__()
        self.vertical_motors = vertical_motors
        super().add_requirement(self.vertical_motors)
        
        self.left_bumper = left_bumper
        self.right_bumper = right_bumper
    
    def initalize(self):
        return 
    
    def execute(self):
        if self.left_bumper():
            self.vertical_motors._set_motor_speeds(0.5, 0, 0)
        elif self.right_bumper():
            self.vertical_motors._set_motor_speeds(0, 0.5, 0.5)
        else:
            self.vertical_motors.stop_motors()

    
    def end(self, interrupted):
        self.vertical_motors.stop_motors()
    
    def is_finished(self):
        return False