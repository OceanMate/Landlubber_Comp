
from jigboard.Jigboard import Jigboard
from structure.Subsystem import Subsystem
from transmission.ComsThread import ComsThread


class Claw(Subsystem):
    def __init__(self):
        super().__init__()
        
        self.clamp_motor = 0
        self.roll_motor = 0
        
    def open_claw(self):
        self._set_clamp_angle(45)  # Set the clamp angle to 45 for open claw
    
    def close_claw(self):
        self._set_clamp_angle(0)
    
    def set_roll_angle(self, angle):
        # Set the roll angle for the claw
        # Ensure the angle is within a valid range, e.g., 0 to 90 degrees
        if angle < 0:
            angle = 0
        elif angle > 90:
            angle = 90
        
        self._set_roll_angle(angle)
    
    def _set_clamp_angle(self, clamp_angle):
        self.clamp_motor = clamp_angle
        
        ComsThread().set_claw_clamp(self.clamp_motor)
    
    def _set_roll_angle(self, roll_angle):
        # Set the roll motor speed based on the roll angle
        self.roll_motor = roll_angle
        
        # Send the command to the ComsThread to set the roll motor
        ComsThread().set_claw_roll(self.roll_motor)

    
    def periodic(self):
        Jigboard().put_string("Claw Motor Angle", 
                             "Clamp: {:.2f} Roll: {:.2f}".format(self.clamp_motor, self.roll_motor))
