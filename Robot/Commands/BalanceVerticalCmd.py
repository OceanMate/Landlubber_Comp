from structure.commands.Command import Command
from Robot.Subsystems.VerticalMotors import VerticalMotors
from jigboard.Jigboard import Jigboard

class BalanceVerticalCmd(Command):
    def __init__(self, vertical_motors : VerticalMotors, left_trigger, right_trigger, right_stick_y, right_bumper, left_bumper, down_dpad):
        super().__init__()
        self.vertical_motors = vertical_motors
        super().add_requirement(self.vertical_motors)
        
        self.left_trigger = left_trigger  # function to get left trigger value (from 0 to 1)
        self.right_trigger = right_trigger # function to get right trigger value (from 0 to 1)
        self.right_stick_y = right_stick_y # function to get right stick y value (from -1 to 1)
        self.right_bumper = right_bumper # function to get right bumper state (True/False)
        self.left_bumper = left_bumper # function to get left bumper state (True/False)
        self.cancel_button = down_dpad # function to get down dpad state (True/False)
    
    def initalize(self):
        Jigboard().put_boolean("Auto Balance Enabled", True)
    
    def execute(self):
            
        right_speed = 0
        if self.right_trigger() > 0.75:
            right_speed = 1
        elif self.right_trigger() > 0:
            right_speed = 0.5

        
        left_speed = 0
        if self.left_trigger() > 0.75:
            left_speed = 1
        elif self.left_trigger() > 0:
            left_speed = 0.5

        
        climb_speed = right_speed - left_speed
        
        pitch_speed = 0
        # add a big deadband since another rotation control is on on the other axis
        if abs(self.right_stick_y()) > 0.25:
            pitch_speed = self.right_stick_y() * 0.5
            
        left_roll_speed = 0
        if self.left_bumper():
            left_roll_speed = 0.5
        
        right_roll_speed = 0
        if self.right_bumper():
            right_roll_speed = 0.5
        
        roll_speed = right_roll_speed - left_roll_speed
        
        if pitch_speed == 0:
            pitch_speed = self.vertical_motors.get_pitch_pid(0)
        if roll_speed == 0:
            roll_speed = self.vertical_motors.get_roll_pid(0)
                
        # speed is from -1 to 1
        self.vertical_motors.run_motors(climb_speed, pitch_speed, roll_speed)
    
    def end(self, interrupted):
        Jigboard().put_boolean("Auto Balance Enabled", False)
    
    def is_finished(self):
        return self.cancel_button()