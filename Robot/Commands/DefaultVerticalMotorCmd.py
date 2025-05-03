from structure.commands.Command import Command

class DefaultVerticalMotorCmd(Command):
    def __init__(self, vertical_motors, left_trigger, right_trigger, right_stick_y):
        super().__init__()
        self.vertical_motors = vertical_motors
        super().add_requirement(self.vertical_motors)
        
        self.left_trigger = left_trigger  # function to get left trigger value (from 0 to 1)
        self.right_trigger = right_trigger # function to get right trigger value (from 0 to 1)
        self.right_stick_y = right_stick_y # function to get right stick y value (from -1 to 1)
    
    def initalize(self):
        return
    
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
            pitch_speed = self.right_stick_y()
            
        # Combine climb_speed and pitch_speed and scale if necessary
        total_speed = abs(climb_speed) + abs(pitch_speed)
        if abs(total_speed) > 1:
            climb_speed /= total_speed
            pitch_speed /= total_speed
        
        # speed is from -1 to 1
        self.vertical_motors.run_motors(climb_speed + pitch_speed, climb_speed - pitch_speed)
    
    def end(self, interrupted):
        self.vertical_motors.stop_motors()
    
    def is_finished(self):
        return False