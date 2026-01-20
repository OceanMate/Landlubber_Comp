from structure.commands.Command import Command
from Robot.Subsystems.LinearMotors import LinearMotors

class TestLinearMotorCmd(Command):
    def __init__(self, linear_motors : LinearMotors, a_button, b_button, x_button, y_button):
        super().__init__()
        self.linear_motors = linear_motors
        super().add_requirement(self.linear_motors)
        
        self.a_button = a_button
        self.b_button = b_button
        self.x_button = x_button
        self.y_button = y_button
    
    def initalize(self):
        return 
    
    def execute(self):        
        if self.a_button():
            self.linear_motors._set_motor_speeds(0.5, 0, 0, 0)
        elif self.b_button():
            self.linear_motors._set_motor_speeds(0, 0.5, 0, 0)
        elif self.x_button():
            self.linear_motors._set_motor_speeds(0, 0, 0.5, 0)
        elif self.y_button():
            self.linear_motors._set_motor_speeds(0, 0, 0, 0.5)
        else:
            self.linear_motors.stop_motors()
    
    def end(self, interrupted):
        self.linear_motors.stop_motors()
    
    def is_finished(self):
        return False